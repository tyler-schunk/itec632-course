"""
A gateway-style model route with a fallback model (Ch. 10, "Step 3. Add Model Router
and Gateway").

The course LiteLLM gateway already does this between its own backends. Here you do
it at the application level, so the app keeps answering even when the main model
alias fails: try PRIMARY first; if that call raises (error or timeout), try FALLBACK.

To test the fallback without breaking anything, the service can SIMULATE a primary
failure, either for one request (header  X-Simulate-Failure: error | timeout) or for
every request (environment variable  SIMULATE_PRIMARY_FAILURE=error | timeout).
  * error   -> the primary call uses a model name that does not exist, so the gateway returns an error
  * timeout -> the primary call gets a 1 ms timeout, so the client raises a timeout error
"""
import inspect
import os
import threading
import time

PRIMARY = os.environ.get("PRIMARY_MODEL", "qwen-moe")
FALLBACK = os.environ.get("FALLBACK_MODEL", "gemma-moe")
PRIMARY_TIMEOUT_S = float(os.environ.get("PRIMARY_TIMEOUT_S", "60"))
FALLBACK_TIMEOUT_S = float(os.environ.get("FALLBACK_TIMEOUT_S", "120"))
SIMULATE_DEFAULT = os.environ.get("SIMULATE_PRIMARY_FAILURE", "").strip().lower()

_MODEL_LOCK = threading.Lock()


class AllModelsFailed(Exception):
    def __init__(self, attempts):
        super().__init__("all models failed")
        self.attempts = attempts


def call_answer(answer_fn, question, history, model, timeout):
    """Call answer_fn with a specific model. Works with answer(question, history, model=, timeout=)
    and, for a Lab 9 answer() without those arguments, by temporarily setting coapp.config.MODEL."""
    params = inspect.signature(answer_fn).parameters
    if "model" in params:
        kwargs = {"model": model}
        if "timeout" in params:
            kwargs["timeout"] = timeout
        return answer_fn(question, history, **kwargs)
    from coapp import config  # older answer(): no model argument
    with _MODEL_LOCK:
        old = config.MODEL
        config.MODEL = model
        try:
            return answer_fn(question, history)
        finally:
            config.MODEL = old


def answer_with_fallback(answer_fn, question, history=None, simulate=None,
                         primary=PRIMARY, fallback=FALLBACK) -> tuple:
    """Try the primary model, then the fallback. Returns (result, attempts).

    attempts is a list like [{"model": "qwen-moe", "ok": False, "error": "...", "latency_s": 0.2},
                             {"model": "gemma-moe", "ok": True, "latency_s": 3.1}].
    Raises AllModelsFailed(attempts) if every model fails.
    """
    simulate = (simulate or SIMULATE_DEFAULT or "").lower()
    attempts = []
    for i, model in enumerate([primary, fallback]):
        use_model, timeout = model, (PRIMARY_TIMEOUT_S if i == 0 else FALLBACK_TIMEOUT_S)
        if i == 0 and simulate == "error":
            use_model = model + "-unavailable"
        if i == 0 and simulate == "timeout":
            timeout = 0.001
        t = time.perf_counter()
        # TODO (Part A, step 6), about 8 lines. Right now the loop only ever tries the primary.
        #   Wrap the call below in try/except Exception as e:
        #     on error:   attempts.append({"model": model, "ok": False,
        #                                  "error": f"{type(e).__name__}: {str(e)[:200]}",
        #                                  "latency_s": round(time.perf_counter() - t, 3)})
        #                 then `continue` so the loop tries the fallback model
        #   on success the code below records the attempt and returns.
        result = call_answer(answer_fn, question, history, use_model, timeout)
        attempts.append({"model": model, "ok": True, "latency_s": round(time.perf_counter() - t, 3)})
        return {**result, "model": model, "fallback_used": i > 0}, attempts
    raise AllModelsFailed(attempts)
