"""
The Co. app v3 (Lab 9 reference): retrieval + tools, with a simple router.

    from coapp.assistant import answer
    out = answer("Which open tickets does Kaw Valley Auto Group have?")
    out["answer"], out["sources"], out["tool_calls"], out["model"], out["latency_s"]

How a question is handled (Ch. 6: RAG for documents, tools for live data):

    route(question) -> "docs"  : retrieve chunks, one model call, no tools     (policies, prices, procedures)
                       "data"  : no retrieval, agent loop with the SQLite tools (tickets, clients, assets)
                       "both"  : retrieve chunks AND offer tools               (e.g. "what's our SLA for KVA's open ticket?")

The router is a few keyword rules on purpose: it is fast, free, and easy to debug.
Lab 15 replaces model choice with a learned/LLM router; this one only decides what
context and tools to offer. Set COAPP_ROUTE=docs|data|both to force a route.

answer() returns the shared course dict
    {"answer", "sources": [{"doc_id", "version", "title"}], "tool_calls": [{"name", "args"}],
     "model", "latency_s"}
plus extra keys for tracing (other code can ignore them):
    "route", "prompt_version", "usage": {"prompt_tokens", "completion_tokens", "total_tokens"},
    "steps": {"retrieve_s", "llm_s", "tools_s", "model_calls"},
    "retrieved": [{"doc_id", "version", "effective_date", "score"}], "retrieval": {...} (as in v2).
Optional keyword arguments (used by Labs 14-15): model=, timeout=.
"""
import json
import re
import sqlite3
import threading
import time

from . import config, prompts
from .retrieve import LAST_INFO, build_index, retrieve
from .tools import TOOLS, call_tool

_INDEX = None
_LOCK = threading.Lock()

DATA_WORDS = re.compile(
    r"\b(tickets?|assets?|laptops?|desktops?|servers?|firewalls?|switch(es)?|access points?|inventory|"
    r"assigned|technician on|open tickets?|how many users|hostnames?|asset tags?|serial|warranty)\b", re.I)
DATA_IDS = re.compile(r"\bTCK-\d{4,7}\b|\bLR-[A-Z]{3}-\d{4}\b", re.I)
DOCS_WORDS = re.compile(
    r"\b(how (do|should|can) (i|we)|how to|procedure|process|policy|policies|runbook|steps?|price|pricing|"
    r"cost|costs|rate|rates|charge|pto|vacation|holiday|business hours|handbook|allowed|should i|escalat\w*|"
    r"include[sd]?|what does .* mean|why)\b", re.I)

_CLIENT_PATTERNS = None


def _client_patterns():
    """Client codes and names from the database, for spotting a client in the question."""
    global _CLIENT_PATTERNS
    if _CLIENT_PATTERNS is None:
        con = sqlite3.connect(f"file:{config.db_path()}?mode=ro", uri=True)
        try:
            rows = con.execute("SELECT code, name FROM clients").fetchall()
        finally:
            con.close()
        names = set()
        for code, name in rows:
            words = re.sub(r"[^a-z0-9& ]", "", name.lower()).split()
            names.add(" ".join(words))
            names.add(" ".join(words[:2]))
        _CLIENT_PATTERNS = ({code for code, _ in rows}, names)
    return _CLIENT_PATTERNS


def mentions_client(question: str) -> bool:
    codes, names = _client_patterns()
    if any(tok in codes for tok in re.findall(r"\b[A-Z]{3}\b", question)):
        return True
    q = " ".join(re.sub(r"[^a-z0-9& ]", " ", question.lower()).split())
    return any(n and n in q for n in names)


def route(question: str) -> str:
    """'docs', 'data' or 'both' (see the module docstring)."""
    if config.ROUTE_MODE in ("docs", "data", "both"):
        return config.ROUTE_MODE
    data = bool(DATA_IDS.search(question) or DATA_WORDS.search(question) or mentions_client(question))
    docs = bool(DOCS_WORDS.search(question))
    if data and docs:
        return "both"
    return "data" if data else "docs"


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


def cited_sources(answer_text: str, chunks: list) -> list:
    """Documents the answer cites as [DOC-ID]; if it cites none, every retrieved document (as in v2)."""
    cited = set(re.findall(r"\[([A-Z][A-Z0-9-]+)\]", answer_text or ""))
    use = [c for c in chunks if c.get("doc_id") in cited] or list(chunks)
    seen, out = set(), []
    for c in use:
        key = (c.get("doc_id"), str(c.get("version")))
        if key not in seen:
            seen.add(key)
            out.append({"doc_id": c.get("doc_id"), "version": str(c.get("version")), "title": c.get("title", "")})
    return out


def _assistant_turn(msg) -> dict:
    """The assistant message (with its tool calls) in the plain-dict form the API expects back."""
    return {"role": "assistant", "content": msg.content or "",
            "tool_calls": [{"id": tc.id, "type": "function",
                            "function": {"name": tc.function.name, "arguments": tc.function.arguments or "{}"}}
                           for tc in msg.tool_calls]}


def answer(question: str, history: list | None = None, *, model: str | None = None,
           timeout: float | None = None) -> dict:
    t0 = time.perf_counter()
    model = model or config.MODEL
    client = config.get_client()
    if timeout is not None:
        client = client.with_options(timeout=timeout, max_retries=0)
    steps = {"retrieve_s": 0.0, "llm_s": 0.0, "tools_s": 0.0, "model_calls": 0}
    usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    which = route(question)
    chunks, info = [], {"retrievers": []}
    if which in ("docs", "both"):
        t = time.perf_counter()
        chunks = retrieve(get_index(), question, k=config.TOP_K)
        info = dict(LAST_INFO)
        steps["retrieve_s"] = time.perf_counter() - t
    messages = prompts.build_messages(question, chunks, history)
    tools = TOOLS if which in ("data", "both") else None

    tool_calls_made, text = [], ""
    rounds = config.MAX_TOOL_ROUNDS if tools else 0
    for round_no in range(rounds + 1):
        offer_tools = tools is not None and round_no < rounds
        t = time.perf_counter()
        resp = client.chat.completions.create(
            model=model, messages=messages, temperature=config.TEMPERATURE, max_tokens=config.MAX_TOKENS,
            extra_body=config.NO_THINK, **({"tools": tools} if offer_tools else {}))
        steps["llm_s"] += time.perf_counter() - t
        steps["model_calls"] += 1
        if resp.usage:
            for key in usage:
                usage[key] += getattr(resp.usage, key, 0) or 0
        msg = resp.choices[0].message
        if offer_tools and msg.tool_calls:
            messages.append(_assistant_turn(msg))
            for tc in msg.tool_calls:
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                t = time.perf_counter()
                result = call_tool(tc.function.name, tc.function.arguments or "{}")
                steps["tools_s"] += time.perf_counter() - t
                tool_calls_made.append({"name": tc.function.name, "args": args})
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
            continue
        text = strip_think(msg.content or "")
        break

    sources = cited_sources(text, chunks)

    return {
        "answer": text,
        "sources": sources,
        "tool_calls": tool_calls_made,
        "model": model,
        "latency_s": round(time.perf_counter() - t0, 3),
        "route": which,
        "prompt_version": getattr(prompts, "PROMPT_VERSION", "?"),
        "usage": usage,
        "steps": {k: (round(v, 3) if isinstance(v, float) else v) for k, v in steps.items()},
        "retrieved": [{"doc_id": c["doc_id"], "version": c["version"], "effective_date": c.get("effective_date"),
                       "score": c.get("score")} for c in chunks],
        "retrieval": info,
    }
