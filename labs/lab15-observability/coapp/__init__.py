"""
Larkspur Co. app, reference implementation v3 (retrieval + tools), shipped with Labs 14-15.

    from coapp.assistant import answer
    answer("What does server management cost?")

Want to use your own Lab 9 version instead? Copy your config.py, prompts.py,
retrieve.py, tools.py and assistant.py over these files. Your answer() must accept
answer(question, history=None) and return the course dict. If it also accepts
model= (as this one does), the Lab 14 fallback route and the Lab 15 router use it;
otherwise they fall back to setting config.MODEL.
"""
__version__ = "3.0-lab14"
