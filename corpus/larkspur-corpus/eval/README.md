# Larkspur gold evaluation set

This folder holds the **gold evaluation set** for the Larkspur help-desk assistant: questions a Larkspur employee or client might really ask, each with a short reference answer written by a person who read the documents. You will use it in several labs (evaluation, model selection, prompting, RAG, monitoring) to measure how well a model or system answers.

Think of it as the "answer sheet" your assistant is graded against. Chapters 3 and 4 of *AI Engineering* explain why a fixed, versioned evaluation set like this matters: without one you can't tell whether a change made the system better or worse.

## Files

| File | What it is |
|---|---|
| `gold_qa.jsonl` | 84 questions, one JSON object per line. |
| `gold_contexts.jsonl` | For each question, the corpus sections a perfect retriever would hand the model (empty for data and some questions). Use it when a lab says "context provided" so you can test the model without testing retrieval. |

## Fields in `gold_qa.jsonl`

```json
{"qid": "Q006", "question": "...", "reference_answer": "...", "source_doc_ids": ["RB-GEN-002"],
 "category": "procedure", "trap": true, "difficulty": "easy"}
```

| Field | Meaning |
|---|---|
| `qid` | Stable ID (`Q001`...). Use it to join results across runs and labs. |
| `question` | The question, as a user would type it. |
| `reference_answer` | The correct answer as of the corpus "today" (2026-11-02). Key fact first, 1-2 sentences. |
| `source_doc_ids` | The `doc_id`(s) from the document front matter that support the answer. Note that some runbooks have more than one version with the same `doc_id`; the answer comes from the **current** one. Empty list for data questions and questions the documents can't answer. |
| `category` | `pricing`, `sla`, `policy` (HR and company policy), `procedure` (runbooks and how things are done), `people`, or `data`. |
| `trap` | `true` if the corpus also contains **another document that gives a different, out-of-date answer**. A good system must notice versions and effective dates and answer from the current one. Which document is out of date is for you to figure out. |
| `difficulty` | `easy` (one lookup), `medium` (read a condition or combine two facts), `hard` (calculation, multi-step reasoning, or several documents). |

## Two special kinds of questions

- **Data questions** (`category: "data"`): the answer is not written in any document. It comes from the SQLite database `data/larkspur.db` (see `data/DATA_DICTIONARY.md`). A document-only assistant should say it can't answer from the documents; an assistant with a SQL tool (Lab 9) should get them right. The ticket table is a sample with some messy labels, so counts are "as labeled in the sample".
- **Unanswerable questions**: the reference answer starts with `Not in the documents.` The right behavior is to say so (abstain), not to guess. These questions measure whether a model makes things up. Many of them come with *related* context that does not contain the answer, which is exactly when models are tempted to guess.

## How to use it

```python
import json
from itec632.corpus import corpus_dir

qa = [json.loads(line) for line in open(corpus_dir() / "eval" / "gold_qa.jsonl")]
ctx = {json.loads(l)["qid"]: json.loads(l)["passages"]
       for l in open(corpus_dir() / "eval" / "gold_contexts.jsonl")}

answerable = [q for q in qa if not q["reference_answer"].startswith("Not in the documents")]
doc_questions = [q for q in answerable if q["category"] != "data"]
```

Each passage in `gold_contexts.jsonl` has `doc_id`, `version`, `effective_date`, `title`, `path`, `section`, and `text`. Passages are sorted by file path, not by importance or date.

Tips:
- Report results **per category** and separately for `trap` and unanswerable questions; an overall average hides the interesting failures.
- Don't tune your prompts on the whole set and then report the score on the same set. If a lab asks you to iterate, hold some questions out.
- Reference answers are short. Exact match will under-count correct but differently worded answers; that is one of the points of Lab 4.
- Found a reference answer you think is wrong? Tell the instructor with the qid and the document that disagrees. Evaluation sets have bugs too.
