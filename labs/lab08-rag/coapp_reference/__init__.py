"""
Larkspur Co. app, reference implementation v2 (retrieval-augmented generation), shipped with Lab 8.
Builds on the Lab 7 v1 reference: same prompts.py, plus retrieve.py.

From the lab08-rag folder:

    from coapp_reference.assistant import answer
    out = answer("What is the after-hours rate for out-of-scope work?")
    out["answer"], out["sources"], out["retrieved"]

Files (course spec, LAB_STYLE_GUIDE section 8):
    config.py     settings (MODEL = qwen-moe, corpus path, retrieval settings)
    prompts.py    SYSTEM_PROMPT, format_chunk(chunk), build_messages(question, context_chunks, history)
    retrieve.py   build_index(docs) -> index; retrieve(index, question, k=5) -> list[Chunk]
    assistant.py  answer(question, history=None) -> dict
    _docs.py      load_docs() fallback for environments without the itec632 helper package
"""
__version__ = "2.0-lab08"
