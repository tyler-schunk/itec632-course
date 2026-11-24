"""
Prompts for the Larkspur help-desk assistant (Lab 7, Part B).

You fill in the TODOs below. The notebook tells you when to edit each one; after saving this file,
rerun the notebook cell that reloads the package.

Chapter 5 ideas to use: clear and explicit instructions, a persona, sufficient context, an explicit
output format, and (from "Defensive Prompt Engineering") delimiters that separate instructions from data.
"""
from . import config

PROMPT_VERSION = "1.0"   # bump this every time you change the prompt, e.g. "1.1" (the notebook asks you to in B4)

# TODO (B1): replace this placeholder with a real system prompt. It should:
#   - say who the assistant is (Larkspur Ridge IT's internal help-desk assistant) and today's date (config.TODAY)
#   - answer ONLY from the provided documents, and cite doc_ids in square brackets, e.g. [PRICE-2026]
#   - say "I don't know based on the documents" when the answer is not there (no guessing)
#   - treat text inside the documents as data, not instructions
#   - keep answers short, key fact first
#
# TODO (B4) - do NOT do this until the notebook's B4 step asks you to (B4 measures the effect of this rule):
#   add a rule for documents that disagree, using version and effective_date.
SYSTEM_PROMPT = f"""You are a helpful assistant. Today is {config.TODAY}."""


def format_chunk(c: dict) -> str:
    """Format one context chunk for the prompt.

    c is a dict with keys: doc_id, version, title, effective_date, text, score.
    TODO (B2): return the text wrapped in clear delimiters (for example <document ...> ... </document>)
    and labeled with doc_id, version, effective_date and title, so the model can cite and compare them.
    """
    return c.get("text", "")


def build_messages(question: str, context_chunks: list, history: list | None = None) -> list:
    """Build the chat messages for one question.

    TODO (B2): return a list that starts with {"role": "system", "content": SYSTEM_PROMPT},
    then any history turns (a list of {"role": "user"|"assistant", "content": ...}; keep the last 6),
    then ONE user message that contains all formatted context chunks (use format_chunk) inside a
    clear delimiter such as <context> ... </context>, followed by the question.
    """
    return [{"role": "user", "content": question}]
