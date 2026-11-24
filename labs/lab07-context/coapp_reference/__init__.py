"""
Larkspur Co. app, reference implementation v1 (prompts + hand-picked context), shipped with Lab 7.

From the lab07-context folder:

    from coapp_reference.assistant import answer
    answer("What are Larkspur's business hours?")                      # uses the default hand-picked docs
    answer("How do I verify a caller?", context_chunks=my_chunks)       # or pass your own context

Files (course spec, LAB_STYLE_GUIDE section 8):
    config.py     settings (MODEL = qwen-moe, corpus path, default context documents)
    prompts.py    SYSTEM_PROMPT, format_chunk(chunk), build_messages(question, context_chunks, history)
    assistant.py  answer(question, history=None, context_chunks=None) -> dict
v1 has no retrieval: Lab 8 adds retrieve.py.
"""
__version__ = "1.0-lab07"
