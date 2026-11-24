"""
The Co. app (v3): retrieval + tools.

    from coapp.assistant import answer
    out = answer("How much is server management per month?")
    out["answer"], out["sources"], out["tool_calls"], out["model"], out["latency_s"]

answer() returns the shared course dict
    {"answer", "sources": [{"doc_id", "version", "title"}], "tool_calls": [{"name", "args"}],
     "model", "latency_s"}
plus three extra keys that Labs 14-15 use for tracing (other code can ignore them):
    "usage": {"prompt_tokens", "completion_tokens", "total_tokens"},
    "steps": {"retrieve_s", "llm_s", "tools_s"},
    "retrieved": [{"doc_id", "version", "score"}].

Optional keyword arguments (Labs 14-15): model= picks the chat model for this call
(the gateway route and router use it), timeout= sets the per-call timeout in seconds.
"""
import json
import re
import threading
import time

from . import config
from .prompts import build_messages
from .retrieve import build_index, retrieve
from .tools import TOOLS, call_tool

_INDEX = None
_LOCK = threading.Lock()
_CITE = re.compile(r"\[([A-Z][A-Z0-9]+(?:-[A-Z0-9]+)+)(?:[ ,][^\]]*)?\]")


def get_index():
    """Build the retrieval index once per process (thread-safe) and reuse it."""
    global _INDEX
    if _INDEX is None:
        with _LOCK:
            if _INDEX is None:
                try:
                    from itec632.corpus import load_docs
                except ImportError:
                    from ._docs import load_docs
                _INDEX = build_index(load_docs())
    return _INDEX


def strip_think(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text or "", flags=re.S).strip()


def cited_doc_ids(text: str) -> list:
    """Doc ids cited like [PRICE-2026] or [RB-ACC-001 v3] in an answer."""
    return list(dict.fromkeys(m.group(1) for m in _CITE.finditer(text or "")))


def answer(question: str, history: list | None = None, *, model: str | None = None,
           timeout: float | None = None) -> dict:
    t0 = time.perf_counter()
    model = model or config.MODEL
    client = config.get_client()
    if timeout is not None:
        client = client.with_options(timeout=timeout, max_retries=0)
    steps = {"retrieve_s": 0.0, "llm_s": 0.0, "tools_s": 0.0}
    usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    t = time.perf_counter()
    chunks = retrieve(get_index(), question, k=config.TOP_K)
    steps["retrieve_s"] = round(time.perf_counter() - t, 3)

    messages = build_messages(question, chunks, history)
    tool_calls_made, text = [], ""
    for round_no in range(config.MAX_TOOL_ROUNDS + 1):
        offer_tools = round_no < config.MAX_TOOL_ROUNDS
        t = time.perf_counter()
        resp = client.chat.completions.create(
            model=model, messages=messages, temperature=config.TEMPERATURE, max_tokens=config.MAX_TOKENS,
            extra_body=config.NO_THINK, **({"tools": TOOLS} if offer_tools else {}))
        steps["llm_s"] += time.perf_counter() - t
        if resp.usage:
            for key in usage:
                usage[key] += getattr(resp.usage, key, 0) or 0
        msg = resp.choices[0].message
        if offer_tools and msg.tool_calls:
            messages.append({"role": "assistant", "content": msg.content or "",
                             "tool_calls": [tc.model_dump() for tc in msg.tool_calls]})
            for tc in msg.tool_calls:
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                t = time.perf_counter()
                result = call_tool(tc.function.name, args)
                steps["tools_s"] += time.perf_counter() - t
                tool_calls_made.append({"name": tc.function.name, "args": args})
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
            continue
        text = strip_think(msg.content or "")
        break

    # Sources: the retrieved documents the answer cites; if it cites none, all retrieved documents.
    cited = set(cited_doc_ids(text))
    seen, sources = set(), []
    for c in chunks:
        key = (c["doc_id"], c["version"])
        if key in seen or (cited and c["doc_id"] not in cited):
            continue
        seen.add(key)
        sources.append({"doc_id": c["doc_id"], "version": c["version"], "title": c["title"]})

    steps = {k: round(v, 3) for k, v in steps.items()}
    return {
        "answer": text,
        "sources": sources,
        "tool_calls": tool_calls_made,
        "model": model,
        "latency_s": round(time.perf_counter() - t0, 3),
        "usage": usage,
        "steps": steps,
        "retrieved": [{"doc_id": c["doc_id"], "version": c["version"], "score": c["score"]} for c in chunks],
    }
