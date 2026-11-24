"""
Larkspur Co. app, reference implementation v3 (retrieval + tools), shipped with Lab 9.
Built on the Lab 8 v2 reference: same config, prompts (plus a tools rule), retrieve; adds tools.py and routing.

Use it as-is from the lab09-agents folder:

    from coapp_reference.assistant import answer
    answer("Which open tickets does Kaw Valley Auto Group have?")

or copy the folder to `coapp/` (the name Labs 14-15 expect) and import `coapp.assistant`.

Files (course spec, LAB_STYLE_GUIDE section 8):
    config.py     settings (MODEL = qwen-moe, corpus paths, retrieval/agent limits)
    prompts.py    SYSTEM_PROMPT, build_messages(question, context_chunks, history)
    retrieve.py   build_index(docs), retrieve(index, question, k=5)  (BM25 + embeddings, RRF)
    tools.py      TOOLS (OpenAI tool schemas), call_tool(name, args) -> str  (read-only SQLite)
    assistant.py  answer(question, history=None) -> dict, with route(): docs | data | both
"""
__version__ = "3.0-lab09"
