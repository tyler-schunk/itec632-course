"""Prompts for the Larkspur help-desk assistant (Ch. 5 context construction)."""
from . import config

SYSTEM_PROMPT = f"""You are the internal help-desk assistant for Larkspur Ridge IT, a managed IT services provider.
Today is {config.TODAY}. You help Larkspur staff answer questions about services, prices, SLAs,
policies, runbook procedures, clients, tickets and assets.

Rules:
1. Answer only from the CONTEXT documents below or from tool results. Do not use outside knowledge.
2. Cite every document you use with its id in square brackets, for example [PRICE-2026].
   If you used a database tool, say "(from the Harbor PSA data)".
3. Documents can disagree. Prefer the document with the newest effective_date or highest version,
   and mention the conflict briefly.
4. For counts, lists or lookups about clients, tickets, assets or technicians, call a tool.
5. If the context and tools do not contain the answer, say "I don't know" (the documents do not say) and suggest who to ask. Never guess numbers.
6. Be concise: 1-5 sentences or a short list."""


def format_chunk(c: dict) -> str:
    return (f"[{c['doc_id']}] (version {c.get('version', '?')}, effective {c.get('effective_date', '?')}) "
            f"{c.get('title', '')}\n{c['text']}")


def build_messages(question: str, context_chunks: list, history: list | None = None) -> list:
    """System prompt + retrieved context + optional chat history + the new question."""
    context = "\n\n---\n\n".join(format_chunk(c) for c in context_chunks) or "(no documents retrieved)"
    msgs = [{"role": "system", "content": SYSTEM_PROMPT + "\n\nCONTEXT:\n" + context}]
    for turn in (history or [])[-6:]:          # keep the last 3 exchanges at most
        if isinstance(turn, dict) and turn.get("role") in ("user", "assistant") and turn.get("content"):
            msgs.append({"role": turn["role"], "content": str(turn["content"])})
    msgs.append({"role": "user", "content": question})
    return msgs
