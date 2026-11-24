# Lab 05: Evaluate AI Systems and Choose a Model

Chapter 4 of *AI Engineering* says that public leaderboards can't tell you which model is right for **your** application. You decide what matters (domain capability, generation quality, instruction following, cost and latency), build an evaluation pipeline on your own data, and let that decide. In this lab you do exactly that for Larkspur Ridge IT: you write evaluation criteria for the help-desk assistant, run all four course chat models on 40 questions from the Larkspur gold set with the documents provided, measure correctness, abstention, latency, and output length, and look closely at **trap questions** where the context contains two documents that disagree. You finish with a weighted scorecard and a model choice you can defend.

**This is a Part-A-only week** (Side Project 1 is due). Part A is graded. Part B (a cost model and build-vs-buy recommendation) is an optional stretch worth up to 10 bonus points.

## Where you'll work

Your Docker JupyterLab on the **KU VPN** (course cluster): `labs/lab05-model-selection/lab05_cluster.ipynb`.

Time: Part A about 2.5 hours (including about 20-30 minutes of waiting while the models run). Part B about 45 minutes.

## Module objectives

| MO | Objective (Bloom level) | CO |
|---|---|---|
| MO 5.1 | **Design** weighted evaluation criteria for a real application using the chapter's four criteria groups (Bloom: Create) | CO2 |
| MO 5.2 | **Build** an evaluation pipeline that combines exact checks (key facts, abstention, format) with an LLM judge (Bloom: Apply) | CO2 |
| MO 5.3 | **Compare** four models on correctness, abstention, latency, and output tokens, and **analyze** how they handle conflicting documents (Bloom: Analyze) | CO2, CO4 |
| MO 5.4 | **Select** a model with a weighted scorecard and **justify** the choice against the chapter's model selection workflow (Bloom: Evaluate) | CO2, CO4 |

## Steps

1. Read Chapter 4: "Evaluation Criteria" (domain-specific, generation, and instruction-following capability; cost and latency), "Model Selection" (including "Model Selection Workflow", "Model Build Versus Buy", and "Navigate Public Benchmarks" with "Data contamination with public benchmarks"), and "Design Your Evaluation Pipeline". The analysis questions cite these sections.
2. Open the notebook with the VPN on and run the Setup cells.
3. **A1:** write your evaluation criteria and weights *before* looking at any results.
4. **A2-A3:** look at the 40-question evaluation set and one trap question's context; finish the key-fact and abstention helpers.
5. **A4-A5:** run all four models (160 requests), then the `qwen-moe` judge (128 requests). Start this early; it takes a while. Everything is cached, so you can stop and resume.
6. **A6-A8:** build the comparison table, the trap-question breakdown, and the weighted scorecard; choose your model.
7. (Optional) **Part B:** cost model and build-vs-buy recommendation.
8. Answer the written analysis and AI-use reflection, run `ck.report()`, save.

## What to submit

`lab05_cluster.ipynb` with all outputs visible, uploaded to Canvas.

## Grading

| Component | Points | How graded |
|---|---|---|
| Auto-checks (Part A, scaled) | 50 | Grading script reads the `ck.report()` line |
| Written analysis | 40 | Uses your own results (15), correct concepts with chapter citation (15), clear reasoning and tradeoffs (10) |
| AI-use reflection | 10 | Complete and specific (10), generic (5), missing (0) |
| Part B stretch (optional) | up to +10 bonus | Bonus checks, reported separately as `partB_bonus_points` |

## Getting unstuck

- **The model run seems stuck:** `qwen-dense` is a 27B dense model and is much slower than the others; that is part of what you are measuring. Watch for the "done in ...s" lines. If the kernel dies or the VPN drops, just re-run: answers already received are cached in `lab05_cache.json`.
- **Lots of `None` verdicts from the judge:** print a few raw judge replies (`call(JUDGE, ...)["text"]`). `parse_verdict()` handles JSON and plain text; if the judge is returning something else, mention it in your analysis rather than fighting it.
- **`is_abstention` test cases fail:** print the failing sentence and write the simplest lowercase regex that matches it without matching the "No. SMS codes are not allowed" case.
- **Your scorecard winner surprises you:** check the direction of each metric (latency and tokens are "lower is better") and your weights. Then ask whether the surprise is a real finding; that's good material for Q1.
- Ask Copilot Chat with the exact error and the cell; check its answer against the TODO hint.
