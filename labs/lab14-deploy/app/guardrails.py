"""
Input and output guardrails for the Co. app service (Ch. 10, "Step 2. Put in Guardrails").

Input guardrail (runs BEFORE anything is sent to the model):
  * redact(text)             -> replaces PII and secrets with placeholders like [REDACTED_EMAIL]
  * is_out_of_scope(text)    -> blocks requests that are not about Larkspur IT work

Output guardrail (runs AFTER the model answers, before the user sees it):
  * check_output(result)     -> strips key-looking strings; requires a citation or "I don't know"

Each function also returns a list of "actions" so the service can report (and in
Lab 15, log) what the guardrail did.
"""
import re

# ---------------------------------------------------------------------------
# Input guardrail 1: PII / secret redaction
# ---------------------------------------------------------------------------
# Order matters: more specific patterns first (an API key can contain digits that
# look like a phone number). Each value is a regular expression.
PII_PATTERNS = {
    # TODO (Part A, step 3): add a pattern for API keys. Course keys look like  sk-abc123...
    #   (sk- followed by 8 or more letters, digits, _ or -). Hint: r"\bsk-[A-Za-z0-9_\-]{8,}"
    "API_KEY": r"(?!x)x",          # placeholder that never matches - replace it
    "PASSWORD": r"(?i)\b(?:password|passwd|pwd)\s*(?:is|:|=)\s*\S+",
    "EMAIL": r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)+",
    # TODO (Part A, step 3): add a pattern for US Social Security numbers like 123-45-6789.
    "SSN": r"(?!x)x",              # placeholder that never matches - replace it
    "CARD": r"\b(?:\d[ \-]?){13,16}\b",
    # TODO (Part A, step 3): add a pattern for US phone numbers: (913) 555-0142, 913-555-0142, 913.555.0142
    "PHONE": r"(?!x)x",            # placeholder that never matches - replace it
}


def redact(text: str) -> tuple:
    """Replace every PII/secret match with [REDACTED_<KIND>]. Returns (new_text, actions)."""
    actions = []
    for kind, pattern in PII_PATTERNS.items():
        text, n = re.subn(pattern, f"[REDACTED_{kind}]", text or "")
        if n:
            actions.append(f"redacted:{kind}x{n}")
    return text, actions


# ---------------------------------------------------------------------------
# Input guardrail 2: scope check
# ---------------------------------------------------------------------------
# Prompt-injection style requests are always blocked.
INJECTION_PATTERNS = [
    r"ignore (all |any )?(the )?(previous|prior|above) (instructions|rules)",
    r"(reveal|show|print) (me )?(your|the) (system prompt|instructions|api key)",
    r"\bjailbreak\b", r"pretend (you are|to be)", r"developer mode",
]
# Topics the help-desk assistant should not handle.
OFF_TOPIC_PATTERNS = [
    r"\b(poem|song|lyrics|haiku|short story|joke)\b", r"\brecipe|cook(ing)?\b", r"\bweather\b",
    r"\b(stocks?|crypto|bitcoin|invest(ing|ment)?)\b", r"\b(football|basketball|baseball|sports?|chiefs|royals)\b",
    r"\b(movie|netflix|tv show)\b", r"\b(homework|essay)\b", r"\b(dating|girlfriend|boyfriend)\b",
    r"\b(diagnos\w*|symptoms?|medication|medical advice|legal advice|lawsuit)\b", r"\bhoroscope\b",
]
# Words that show the request IS about Larkspur's IT work, even if an off-topic word appears.
IN_SCOPE_WORDS = [
    "larkspur", "ticket", "client", "sla", "price", "pricing", "cost", "tier", "runbook", "printer",
    "password", "mfa", "laptop", "desktop", "onsite", "backup", "vpn", "email", "outlook", "server",
    "network", "wi-fi", "wifi", "technician", "on-call", "pto", "handbook", "policy", "asset", "invoice",
    "rate", "essentials", "professional", "premier", "m365", "microsoft", "onboarding", "offboarding",
    "firewall", "phone", "voip", "harbor", "atlas", "beacon", "vaultline", "pagerline", "windows",
]


def is_out_of_scope(text: str) -> tuple:
    """Return (blocked, reason). reason is "" when the request is allowed."""
    # Ignore redaction placeholders: "[REDACTED_EMAIL]" must not count as the in-scope word "email".
    low = re.sub(r"\[REDACTED_\w+\]", " ", text or "").lower()
    # TODO (Part A, step 4), about 6 lines:
    #   1. If any INJECTION_PATTERNS regex matches `low` -> return True, "prompt_injection"
    #   2. off_topic = any OFF_TOPIC_PATTERNS regex matches `low`
    #      on_topic  = any IN_SCOPE_WORDS word starts a word in `low`: re.search(r"\b" + re.escape(w), low)
    #   3. If off_topic and not on_topic -> return True, "off_topic"
    #   Use re.search(pattern, low).
    return False, ""


REFUSAL = ("I can only help with Larkspur Ridge IT work: services, prices, SLAs, policies, runbooks, "
           "clients, tickets and assets. Please rephrase your question, or ask your team lead.")

# ---------------------------------------------------------------------------
# Output guardrail
# ---------------------------------------------------------------------------
KEY_PATTERNS = [
    r"\bsk-[A-Za-z0-9_\-]{8,}", r"\bAKIA[0-9A-Z]{16}\b", r"\bghp_[A-Za-z0-9]{20,}",
    r"(?i)bearer\s+[A-Za-z0-9._\-]{16,}", r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*\S{8,}",
]
CITATION = re.compile(r"\[([A-Z][A-Z0-9]+(?:-[A-Z0-9]+)+)(?:[ ,][^\]]*)?\]")
DONT_KNOW = re.compile(r"(?i)\b(i don'?t know|i do not know|not sure|couldn'?t find|could not find|"
                       r"no information|not (in|found in|mentioned in|covered (in|by)) the (context|documents|data)|"
                       r"(documents|context|sources) (do not|don'?t|does not|doesn'?t) "
                       r"(say|mention|specify|include|contain|state))")
NO_SOURCE_MESSAGE = ("I don't know. I couldn't find a Larkspur document or data record that supports an "
                     "answer, so I won't guess. Try rephrasing, or ask the Service Desk lead.")


def has_citation(result: dict, known_doc_ids=None) -> bool:
    """True if the answer cites a document id (that exists, when known_doc_ids is given) or used a tool."""
    text = result.get("answer", "") or ""
    cited = [m.group(1) for m in CITATION.finditer(text)]
    if known_doc_ids is not None:
        cited = [c for c in cited if c in known_doc_ids]
    return bool(cited) or bool(result.get("tool_calls")) or "harbor psa data" in text.lower()


def check_output(result: dict, known_doc_ids=None) -> tuple:
    """Apply the output guardrail to an answer() dict. Returns (result, actions)."""
    actions = []
    text = result.get("answer", "") or ""
    for p in KEY_PATTERNS:
        text, n = re.subn(p, "[REDACTED_KEY]", text)
        if n:
            actions.append(f"stripped_key x{n}")
    result = {**result, "answer": text}
    # TODO (Part A, step 5), about 3 lines: if the answer has no citation (use has_citation)
    #   AND does not say it doesn't know (DONT_KNOW.search(text) is None), then
    #   append "no_citation_replaced" to actions and replace the answer:
    #   result = {**result, "answer": NO_SOURCE_MESSAGE, "sources": []}
    return result, actions
