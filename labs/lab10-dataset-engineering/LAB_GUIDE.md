# Lab 10 - Dataset Engineering

A fine-tuned model is only as good as the data it learns from. Next week (Lab 11) you fine-tune a small model on Colab; this week you build its training data the way an AI engineer at Larkspur would. First you audit the real Harbor PSA ticket data for quality problems (duplicates, wrong labels, useless notes) and clean it. Then you build a supervised fine-tuning (SFT) dataset: question/answer pairs **generated** by `qwen-moe` from current Larkspur documents and **filtered** by an AI judge and simple rules, plus real "ticket -> resolution note" pairs from the cleaned tickets, all with recorded lineage. This lab covers **Chapter 8** of *AI Engineering* (data curation and quality, data synthesis and verification, deduplication, cleaning and formatting) and the **"When to Finetune"** part of **Chapter 7**. (The course swaps the Chapter 7 and 8 order on purpose, so you fine-tune on data you built.)

## Where you'll work

- **Cluster notebook:** `lab10_cluster.ipynb` in your local Docker JupyterLab, with the **KU VPN** on.
- **Time:** about 4-5 hours. The generation and judging steps take about 10-15 minutes of waiting in total.
- **Cluster use:** about 150 requests (embeddings are batched; generation and judging run 3 requests at a time).

## Module objectives

| MO | Objective | CO |
|---|---|---|
| MO 10.1 | **Assess** a real dataset against the chapter's data quality dimensions and find label noise and duplicates (Bloom: Evaluate) | CO4 |
| MO 10.2 | **Apply** embedding-based near-duplicate detection and a neighbor-vote plus LLM relabeling pass to flag suspicious labels (Bloom: Apply) | CO2, CO4 |
| MO 10.3 | **Construct** a synthetic, source-grounded instruction dataset with an AI judge and heuristic filters (Bloom: Create) | CO4 |
| MO 10.4 | **Justify** curation decisions (current-only sources, filters, cutoffs, test-set leakage checks) and document data lineage (Bloom: Evaluate) | CO4, CO5 |

## Steps

1. Read Chapter 8: "A Data-Centric View of AI", "Data Curation" (especially "Data Quality" and "Data Quantity"), "Data Augmentation and Synthesis" (especially "AI-Powered Data Synthesis" with "Data verification" and "Limitations to AI-generated data"), and "Data Processing" ("Inspect Data", "Deduplicate Data", "Clean and Filter Data", "Format Data"). Then read the "When to Finetune" section of Chapter 7 ("Reasons to Finetune", "Reasons Not to Finetune", and "Finetuning and RAG").
2. Open `labs/lab10-dataset-engineering/lab10_cluster.ipynb` and run **Run > Run All Cells** once to see the checks.
3. **Part A (guided):**
   - A1: profile the ticket data and map each problem to a data quality dimension.
   - A2: embed all tickets and find near-duplicate submissions (pick your similarity threshold from the sweep).
   - A3: flag suspicious categories with a nearest-neighbor vote, then relabel a sample with `qwen-moe`, including a control group.
   - A4: clean the data (dedupe, drop disputed labels, mark usable notes).
4. **Part B (applied):**
   - B1: keep only **current** documents (newest version; non-runbooks effective 2025 or later).
   - B2: generate grounded question/answer pairs and verify their evidence.
   - B3: filter with an AI judge (`gemma-moe`) and heuristics; remove near-duplicate questions.
   - B4: select real ticket/resolution-note pairs from cleaned tickets created on or after 2025-06-02.
   - B5: format as chat JSONL, split 40 test examples, check for train/test leakage, save with lineage.
5. Check that `my_dataset/larkspur_sft_train.jsonl` and `my_dataset/larkspur_sft_test.jsonl` exist. **Keep them for Lab 11.**
6. Answer the four written-analysis questions and the AI-use reflection, run the final cell, save.

## What to submit

- `lab10_cluster.ipynb` **with outputs**, uploaded to Canvas.
- Keep (don't upload) the two JSONL files in `my_dataset/`; you upload them to Colab next week.
- If your dataset build fails or ends up far too small, you can still do Lab 11 with the pre-built set in `fallback_dataset/` (Lab 11 uses it automatically). Explain what went wrong in your analysis.

## Grading

| Component | Points | How graded |
|---|---|---|
| Auto-checks (32 check points scaled to 50) | 50 | Grading script reads the `ck.report()` line |
| Written analysis | 40 | Uses your own results (15), correct concepts with chapter citation (15), clear reasoning and tradeoffs (10) |
| AI-use reflection | 10 | Complete and specific (10), generic (5), missing (0) |

## Getting unstuck

- **Lots of `(qwen-moe: ...)` or `(gemma-moe: ...)` error lines.** Those are failed structured-output calls. A few are normal and the pipeline skips them; if most fail, re-run the cell (rate limit) or check your VPN. The judge falls back to `qwen-moe` automatically if `gemma-moe` errors.
- **Hundreds of duplicate pairs, or none.** Look at the threshold sweep and the printed examples, then set `DUP_THRESHOLD`. Duplicate *submissions* are the same requester, minutes apart. Several different people reporting the same outage are related tickets, not duplicates: say how you handled them.
- **Very few pairs survive B3.** Look at the funnel table. If `grounded` drops most pairs, print a few `evidence` strings next to their source: the model may be paraphrasing instead of copying. Try the optional fuzzy match in `grounded()`.
- **Fewer than 200 training examples.** Raise `N_CHUNKS` (each extra section is about 2 requests) or `N_TICKETS`, and explain the change. Don't loosen the judge threshold without saying why.
- Ask Copilot Chat with the exact error message and the cell. For data questions, paste 2-3 example rows, not the whole file.
