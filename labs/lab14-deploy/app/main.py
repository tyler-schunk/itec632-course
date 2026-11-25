"""
Larkspur Co. app as a web service (Lab 14).

    uvicorn app.main:app --host 0.0.0.0 --port 8000

Endpoints
    GET  /health    -> {"status": "ok", ...}            (cheap: never calls a model)
    POST /ask       -> the Co. app answer dict, after the input and output guardrails
         body: {"question": "...", "history": [{"role": "user"|"assistant", "content": "..."}]}
         optional header  X-Simulate-Failure: error | timeout   (tests the fallback route)

The request path, following Ch. 10's architecture:
    input guardrail (redact PII/secrets, block out-of-scope)
      -> model gateway route (primary model, fallback model)
          -> Co. app v3 (retrieval + tools)
      -> output guardrail (strip keys, require a citation or "I don't know")
"""
import threading
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from coapp.assistant import answer, get_index

from . import gateway, guardrails

SERVICE_VERSION = "lab14-1.0"
_state = {"index_ready": False, "index_error": None, "known_doc_ids": None}


def _warm_index():
    """Build the retrieval index in the background so /health answers right away."""
    try:
        idx = get_index()
        _state["known_doc_ids"] = {c["doc_id"] for c in idx["chunks"]}
        _state["index_ready"] = True
        if idx.get("embed_error"):
            _state["index_error"] = "embeddings unavailable, BM25 only: " + idx["embed_error"][:200]
    except Exception as e:
        _state["index_error"] = f"{type(e).__name__}: {e}"[:300]


@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Thread(target=_warm_index, daemon=True).start()
    yield


app = FastAPI(title="Larkspur Co. app", version=SERVICE_VERSION, lifespan=lifespan)


class Turn(BaseModel):
    role: str
    content: str


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    history: list[Turn] | None = None


@app.get("/health")
def health():
    # TODO (Part A, step 2): add a "status" key with the value "ok" as the first key below.
    # Monitoring tools look for it (Docker's HEALTHCHECK only checks that /health answers).
    return {
        "service": "larkspur-coapp",
        "version": SERVICE_VERSION,
        "index_ready": _state["index_ready"],
        "index_error": _state["index_error"],
        "primary_model": gateway.PRIMARY,
        "fallback_model": gateway.FALLBACK,
    }


@app.post("/ask")
def ask(req: AskRequest, x_simulate_failure: str | None = Header(default=None)):
    t0 = time.perf_counter()

    # 1. Input guardrail: redact PII/secrets in the question and the history.
    question, input_actions = guardrails.redact(req.question)
    history = []
    for turn in req.history or []:
        content, acts = guardrails.redact(turn.content)
        input_actions += acts
        history.append({"role": turn.role, "content": content})

    # 2. Input guardrail: block out-of-scope requests before spending a model call.
    blocked, reason = guardrails.is_out_of_scope(question)
    if blocked:
        return {
            "answer": guardrails.REFUSAL, "sources": [], "tool_calls": [], "model": "none",
            "latency_s": round(time.perf_counter() - t0, 3),
            "blocked": True, "fallback_used": False, "attempts": [],
            "guardrails": {"input": input_actions + [f"blocked:{reason}"], "output": []},
        }

    # 3. Gateway route: primary model, then fallback.
    try:
        result, attempts = gateway.answer_with_fallback(answer, question, history or None,
                                                        simulate=x_simulate_failure)
    except gateway.AllModelsFailed as e:
        raise HTTPException(status_code=502, detail={"error": "all models failed", "attempts": e.attempts})

    # 4. Output guardrail.
    if _state["known_doc_ids"] is None:
        _state["known_doc_ids"] = {c["doc_id"] for c in get_index()["chunks"]}
    result, output_actions = guardrails.check_output(result, _state["known_doc_ids"])

    result.update({
        "latency_s": round(time.perf_counter() - t0, 3),   # whole request, including guardrails
        "blocked": False,
        "attempts": attempts,
        "guardrails": {"input": input_actions, "output": output_actions},
    })
    return result
