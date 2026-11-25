"""
Larkspur Co. app service, Lab 15: router + tracing + user feedback.

    uvicorn app.main:app --host 0.0.0.0 --port 8000

Endpoints
    GET  /health              cheap status (never calls a model)
    POST /ask                 {"question", "history"?, "session_id"?}  -> answer dict + request_id + disclosure
                              optional headers: X-Simulate-Failure: error|timeout, X-Client-Run: <tag>
    POST /feedback            {"request_id", "rating": "up"|"down", "comment"?}
    GET  /traces?limit=200    recent traces from memory (lab convenience; protect or remove in production)

Request path (Ch. 10):
    input guardrail -> router (small vs large model) -> gateway route with fallback
      -> Co. app v3 (retrieval + tools) -> output guardrail -> trace (JSONL)
"""
import threading
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, Field

from coapp.assistant import answer, get_index

from . import gateway, guardrails, router, tracing

SERVICE_VERSION = "lab15-1.0"
DISCLOSURE = ("AI-generated answer: written by an AI assistant from Larkspur documents and data. "
              "It can be wrong; check the cited sources before acting on it.")
FALLBACK_FOR = {router.SMALL: router.LARGE, router.LARGE: gateway.FALLBACK}
_state = {"index_ready": False, "index_error": None, "known_doc_ids": None}


def _warm_index():
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
    session_id: str | None = Field(default=None, max_length=64)


class FeedbackRequest(BaseModel):
    request_id: str = Field(min_length=1, max_length=64)
    rating: Literal["up", "down"]
    comment: str | None = Field(default=None, max_length=1000)


@app.get("/health")
def health():
    return {
        "status": "ok", "service": "larkspur-coapp", "version": SERVICE_VERSION,
        "index_ready": _state["index_ready"], "index_error": _state["index_error"],
        "router_mode": router.MODE, "small_model": router.SMALL, "large_model": router.LARGE,
        "fallback_model": gateway.FALLBACK, "log_writable": tracing.status["log_writable"],
        "trace_file": str(tracing.TRACE_FILE),
    }


@app.post("/ask")
def ask(req: AskRequest, x_simulate_failure: str | None = Header(default=None),
        x_client_run: str | None = Header(default=None)):
    request_id = tracing.new_request_id()
    trace = tracing.Trace(request_id)
    trace.set(service_version=SERVICE_VERSION, session_id=req.session_id, client_run=x_client_run,
              history_turns=len(req.history or []))

    # 1. Input guardrail: redact, then scope check.
    with trace.step("input_guardrail"):
        question, input_actions = guardrails.redact(req.question)
        history = []
        for turn in req.history or []:
            content, acts = guardrails.redact(turn.content)
            input_actions += acts
            history.append({"role": turn.role, "content": content})
        blocked, reason = guardrails.is_out_of_scope(question)
    # TODO (Part A, step A4): this logs the RAW question, including any email, phone number or key
    # the user typed. Log the redacted version from the input guardrail step above instead.
    trace.set(question=req.question)

    if blocked:
        result = {"answer": guardrails.REFUSAL, "sources": [], "tool_calls": [], "model": "none",
                  "blocked": True, "fallback_used": False, "attempts": [],
                  "guardrails": {"input": input_actions + [f"blocked:{reason}"], "output": []}}
        trace.set(route={"route": "blocked", "model": "none", "reason": reason}, model="none", blocked=True,
                  guardrails=result["guardrails"], usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                  retrieved=[], sources=[], tool_calls=[], attempts=[], fallback_used=False, status=200,
                  answer=result["answer"])
        rec = trace.finish()
        return {**result, "latency_s": rec["latency_s"], "request_id": request_id,
                "route": "blocked", "disclosure": DISCLOSURE}

    # 2. Router: pick the model for this question.
    with trace.step("route"):
        decision = router.choose_route(question)
    trace.set(route=decision)

    # 3. Gateway route with fallback (routed model first).
    primary = decision["model"]
    try:
        with trace.step("answer"):
            result, attempts = gateway.answer_with_fallback(
                answer, question, history or None, simulate=x_simulate_failure,
                primary=primary, fallback=FALLBACK_FOR.get(primary, gateway.FALLBACK))
    except gateway.AllModelsFailed as e:
        trace.set(model=None, blocked=False, attempts=e.attempts, status=502, error="all models failed",
                  guardrails={"input": input_actions, "output": []},
                  usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0})
        trace.finish()
        raise HTTPException(status_code=502, detail={"error": "all models failed", "attempts": e.attempts,
                                                     "request_id": request_id})

    # 4. Output guardrail.
    with trace.step("output_guardrail"):
        if _state["known_doc_ids"] is None:
            _state["known_doc_ids"] = {c["doc_id"] for c in get_index()["chunks"]}
        result, output_actions = guardrails.check_output(result, _state["known_doc_ids"])

    guard = {"input": input_actions, "output": output_actions}
    inner = result.get("steps", {})
    trace.record["steps"].update({k: v for k, v in inner.items() if k in ("retrieve_s", "llm_s", "tools_s")})
    trace.set(model=result.get("model"), fallback_used=result.get("fallback_used", False), attempts=attempts,
              blocked=False, guardrails=guard, status=200,
              usage=result.get("usage", {}), router_tokens=decision.get("router_tokens", 0),
              retrieved=[r["doc_id"] for r in result.get("retrieved", [])],
              sources=[s["doc_id"] for s in result.get("sources", [])],
              tool_calls=result.get("tool_calls", []),
              answer=guardrails.redact(result.get("answer", ""))[0][:1000])
    rec = trace.finish()

    result.update({"latency_s": rec["latency_s"], "blocked": False, "attempts": attempts, "guardrails": guard,
                   "request_id": request_id, "route": decision["route"], "disclosure": DISCLOSURE})
    return result


@app.post("/feedback")
def feedback(fb: FeedbackRequest):
    # FastAPI has already checked that rating is "up" or "down" (otherwise it answered 422).
    trace = tracing.find_trace(fb.request_id)
    # TODO (Part A, step A3), about 8 lines:
    #   1. If no trace has this request_id, answer 404 (raise an HTTPException with a short detail).
    #   2. Redact the comment with guardrails.redact() if there is one (never store raw PII);
    #      redact() returns a tuple, and you want the text.
    #   3. Build one record with these keys: request_id, ts (tracing.now_iso()), rating, comment
    #      (the redacted one), and from the trace: route (the "route" field inside the trace's
    #      route dict, which may be missing), model, session_id, client_run.
    #   4. Append the record to tracing.FEEDBACK_FILE (tracing has a JSONL helper).
    #   5. Return a small dict: status "recorded" and the request_id.
    raise HTTPException(status_code=501, detail="TODO: /feedback is not implemented yet")


@app.get("/traces")
def traces(limit: int = Query(default=200, ge=1, le=2000), client_run: str | None = None):
    rows = tracing.recent_traces(2000)
    if client_run:
        rows = [r for r in rows if r.get("client_run") == client_run]
    return rows[-limit:]
