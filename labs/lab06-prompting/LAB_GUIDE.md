# Lab 06 - Prompt Engineering Fundamentals: Roles, Structured Output, and a Ticket Classifier

Chapter 5 of *AI Engineering* opens with the basics of prompting: what a prompt is made of, zero-shot instructions, and the split between system and user prompts. This lab turns those ideas into working code. You'll see how the chat template turns messages into one string, write clear zero-shot instructions, get reliably parseable answers with strict JSON-schema output, and treat prompts as versioned code. Then you'll build a real tool for Larkspur Ridge IT: a classifier that pre-fills the category and priority of help-desk tickets. You'll measure it with two models, compare cost and latency, and find out that the "correct" labels are not always correct.

## Where you'll work

- **Cluster notebook:** `lab06_cluster.ipynb` in your Docker JupyterLab, on the KU VPN.
- **Time:** about 4-5 hours (about 1.5 hours for Part A, 2 hours for Part B, 1 hour for the analysis).
- **Cluster use:** about 260 requests. The batch step paces itself and caches results in `lab06_results.jsonl`, so rerunning the notebook does not repeat those requests.

## Module objectives

| MO | Objective | CO |
|---|---|---|
| MO 6.1 | Explain how system prompts, user prompts, and the chat template combine into the input a model sees (Bloom: Understand) | CO1, CO2 |
| MO 6.2 | Apply clear zero-shot instructions and strict JSON-schema structured output to get reliable, machine-readable model responses (Bloom: Apply) | CO2 |
| MO 6.3 | Implement versioned prompt templates and use them to compare prompt changes on the same data (Bloom: Apply) | CO2 |
| MO 6.4 | Evaluate a small and a large model on a ticket classification task using accuracy, a confusion matrix, latency, and cost (Bloom: Evaluate) | CO2 |
| MO 6.5 | Analyze model-label disagreements to judge whether the model or the human label is wrong (Bloom: Analyze) | CO2 |

## Steps

1. Read Chapter 5, "Introduction to Prompting" (including "In-Context Learning: Zero-Shot and Few-Shot", "System Prompt and User Prompt", and "Context Length and Context Efficiency"), plus "Organize and Version Prompts" from "Prompt Engineering Best Practices". Skim Chapter 2, "Structured Outputs", and Chapter 4, "Cost and Latency" (under "Evaluation Criteria").
2. Start Docker (`docker compose up`), connect to the VPN, and open `labs/lab06-prompting/lab06_cluster.ipynb`.
3. Run the setup cell. It should print a reply and a green check.
4. **Part A** (guided practice). Work through A1-A4. Each section has a short explanation, an example to run, a small TODO, and a check cell:
   - A1: system versus user prompt, and the chat template.
   - A2: vague versus clear zero-shot instructions.
   - A3: JSON mode versus a strict JSON schema, validated with pydantic and jsonschema.
   - A4: a versioned prompt registry.
5. **Part B** (applied lab). Classify about 100 Larkspur tickets with `qwen-small` and `qwen-moe`:
   - B1-B2: load the tickets and finish `classify()`.
   - B3: run both models, then compute accuracy and confusion matrices.
   - B4: compare cost and latency.
   - B5: review at least 8 disagreements and judge who is right.
6. Answer the four **written analysis** questions using your own numbers, and cite the chapter where asked.
7. Complete the **AI-use reflection**.
8. Run the notebook top to bottom (**Run > Run All Cells**). Results come from the cache, so this is quick. Check that the final `ck.report()` cell printed, then save.

## What to submit

Upload `lab06_cluster.ipynb` **with its outputs** to Canvas. You don't need to upload `lab06_results.jsonl` or `prompts_lab06.json`.

## Grading

| Component | Points | How graded |
|---|---|---|
| Auto-checks | 50 | The grading script reads the summary line printed by `ck.report()` and scales your check score to 50 |
| Written analysis | 40 | Uses your own results (15), correct concepts with chapter citation (15), clear reasoning and trade-offs (10) |
| AI-use reflection | 10 | Complete and specific (10), generic (5), missing (0) |

## Getting unstuck

- **A JSON-schema call fails with a 400 error:** print `TRIAGE_SCHEMA`. Strict mode wants every property listed in `required`, `"additionalProperties": False`, and enum values that are plain strings.
- **`classify()` returns None, or B3 says "finish B2 first":** you still have `messages = None` or `response_format=None` in `classify()`. Fill in both lines and rerun the B2 cell before B3.
- **B3 was interrupted (VPN dropped, rate limit):** just rerun the cell. Finished results come from `lab06_results.jsonl`. If you change your prompt, its fingerprint changes and the runner makes fresh requests for it (another ~200 requests). Only do that on purpose.
- **Accuracy looks low:** before you change the prompt, look at the confusion matrix and a few rows of `res`. Some "errors" are the label's fault, not the model's. That's what B5 is for.
- **Anything else:** ask Copilot Chat about the exact error message, and paste in the cell that caused it.
