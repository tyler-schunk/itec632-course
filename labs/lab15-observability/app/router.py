"""
Model router (Ch. 10, "Step 3. Add Model Router and Gateway").

Not every question needs the big model. A router looks at the query BEFORE the
expensive call and picks a model: short single-fact lookups go to the small, cheap
qwen-small; multi-step, comparative or data questions go to qwen-moe.

Modes (environment variable ROUTER_MODE):
    heuristic   (default) keyword/length rules only - free and instant
    hybrid      heuristic first; if it says "small", ask the qwen-small classifier to confirm
    classifier  always ask the qwen-small classifier (one extra small model call per request)
    large_only  send everything to the large model (the baseline without routing)
"""
import json
import os
import re
import time

SMALL = os.environ.get("ROUTER_SMALL_MODEL", "qwen-small")
LARGE = os.environ.get("ROUTER_LARGE_MODEL", "qwen-moe")
MODE = os.environ.get("ROUTER_MODE", "heuristic").strip().lower()

# Cues that a question needs reasoning, several facts, or a careful reading of conditions.
COMPLEX_CUES = [
    "why", "explain", "compare", "difference", "versus", " vs ", "steps", "step by step", "procedure",
    "how do i", "how should", "what should", "calculate", "total", "if ", "when should", "both",
    "which one", "and what", "and who", "and how", "and when", "walk me through", "best way",
]
# Cues that the answer comes from the database (tool use works better on the large model).
DATA_CUES = [
    "how many", "which client", "which clients", "most ", "average", "list ", "count", "number of",
    "tck-", "lr-", "assigned", "in the sample", "inventory",
]
MAX_SIMPLE_WORDS = 18


def classify_heuristic(question: str) -> tuple:
    """Return (route, reason) with route "small" or "large"."""
    q = " " + (question or "").lower().strip() + " "
    n_words = len(q.split())
    # TODO (Part A, step A1), about 10 lines. Check in this order and return the FIRST rule that fires:
    #   1. a cue from DATA_CUES appears in q     -> "large", reason "data_cue:" + that cue without spaces
    #   2. a cue from COMPLEX_CUES appears in q  -> "large", reason "complex_cue:" + that cue without spaces
    #   3. more words than MAX_SIMPLE_WORDS      -> "large", reason "long_question"
    #   4. more than one question mark           -> "large", reason "multi_part"
    #   5. none of the above                     -> "small", reason "short_lookup"
    # Until you do this, every question goes to the large model (no routing).
    return "large", "todo_not_routed"


CLASSIFIER_PROMPT = (
    "You route questions for an IT company's help-desk assistant. Reply with JSON only: "
    '{"label": "simple"} if the question asks for ONE fact that a single document sentence answers '
    '(a price, a phone number, a target time), or {"label": "complex"} if it needs several facts, '
    "conditions, a calculation, steps, a comparison, or a database lookup.")


def classify_with_model(question: str, client=None) -> tuple:
    """Ask qwen-small to label the question. Returns (route, reason, usage_tokens)."""
    if client is None:
        from coapp import config
        client = config.get_client()
    resp = client.chat.completions.create(
        model=SMALL, temperature=0, max_tokens=20,
        messages=[{"role": "system", "content": CLASSIFIER_PROMPT}, {"role": "user", "content": question}],
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )
    text = resp.choices[0].message.content or ""
    tokens = getattr(resp.usage, "total_tokens", 0) if resp.usage else 0
    m = re.search(r"\{.*?\}", text, re.S)
    label = ""
    try:
        label = json.loads(m.group(0)).get("label", "") if m else ""
    except (json.JSONDecodeError, AttributeError):
        pass
    label = label or ("simple" if "simple" in text.lower() else "complex")
    return ("small" if label == "simple" else "large"), f"classifier:{label}", tokens


def choose_route(question: str, mode: str | None = None) -> dict:
    """Pick a model for this question. Never raises: on classifier errors it falls back to the heuristic."""
    mode = (mode or MODE).lower()
    t = time.perf_counter()
    tokens = 0
    if mode == "large_only":
        route, reason = "large", "large_only"
    else:
        route, reason = classify_heuristic(question)
        if mode == "classifier" or (mode == "hybrid" and route == "small"):
            try:
                route, reason, tokens = classify_with_model(question)
            except Exception as e:
                reason += f" (classifier failed: {type(e).__name__})"
    return {"route": route, "model": SMALL if route == "small" else LARGE, "reason": reason,
            "mode": mode, "router_latency_s": round(time.perf_counter() - t, 4), "router_tokens": tokens}
