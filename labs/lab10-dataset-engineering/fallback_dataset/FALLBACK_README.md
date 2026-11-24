# FALLBACK dataset (use only if your own Lab 10 dataset failed)

These two files are a **pre-built fallback** so you can still do Lab 11 if your Lab 10 build did not finish or came out too small:

- `FALLBACK_larkspur_sft_train.jsonl` - 252 training examples
- `FALLBACK_larkspur_sft_test.jsonl` - 40 held-out test examples (20 doc Q&A + 20 ticket notes)

Same format as the Lab 10 notebook output: one JSON object per line, `{"messages": [system, user, assistant], "meta": {...}}`. The `meta` object is the lineage (source document and version, or ticket ID).

How it was made (no LLM involved, so it is *not* the same as what your pipeline produces):
- Doc Q&A from **current** documents only: runbook sections (purpose, prerequisites, priority guidance, escalation, ticket notes) turned into question/answer pairs by a script, plus hand-written questions whose supporting text was checked against the cited document.
- Ticket -> resolution note pairs from real closed tickets created on or after 2025-06-02, with clean, complete notes.

Lab 11 uses these automatically when it can't find your own files. **Say in your Lab 11 analysis that you used the fallback.**
