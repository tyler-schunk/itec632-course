# Lab 07 - Context Construction and Prompt Iteration (Co. app v1)

Chapter 5 of *AI Engineering* moves from "what is a prompt" to how to engineer one well: provide sufficient context, use examples, break tasks into steps, iterate and version your prompts, and defend them against prompt attacks. In this lab you practice each of those with measurements. Then you build **version 1 of the Larkspur company assistant** (the Co. app), which answers staff questions from documents you hand it. Larkspur keeps old document versions around, and some contradict the current ones, so your assistant has to learn to use version and date metadata to pick the right answer.

## Where you'll work

- **Cluster notebook:** `lab07_cluster.ipynb` in your Docker JupyterLab, on the KU VPN. You also edit one Python file, `coapp/prompts.py`, in the JupyterLab editor.
- **Time:** about 4-5 hours: about 1.5-2 hours for Part A, 1.5-2 hours for Part B, and 1 hour for the analysis. A3 is optional practice; skip it if you're short on time.
- **Cluster use:** about 190 requests. Part B results are cached in `lab07_app_results.jsonl`, so reruns are cheap.

## Module objectives

| MO | Objective | CO |
|---|---|---|
| MO 7.1 | Distinguish instructions from context and construct prompts that keep them separate with delimiters (Bloom: Apply) | CO2 |
| MO 7.2 | Measure how few-shot example number, order, and wording affect output stability (Bloom: Analyze) | CO2 |
| MO 7.3 | Apply prompt versioning and a dev-set evaluation loop to improve a prompt (Bloom: Apply) | CO2 |
| MO 7.4 | Evaluate prompt-level and system-level defenses against indirect prompt injection (Bloom: Evaluate) | CO2, CO5 |
| MO 7.5 | Build a company assistant that uses document version metadata to resolve conflicting sources (Bloom: Create) | CO2, CO3 |

## Steps

1. Read Chapter 5, "Prompt Engineering Best Practices" (especially "Provide Sufficient Context", "Break Complex Tasks into Simpler Subtasks", "Iterate on Your Prompts", and "Organize and Version Prompts") and "Defensive Prompt Engineering" (especially "Indirect prompt injection" and "Defenses Against Prompt Attacks"). Revisit "In-Context Learning: Zero-Shot and Few-Shot" from last week before A2.
2. Skim `corpus/larkspur-corpus/eval/README.md`. It explains the gold questions and the hand-picked contexts you'll use.
3. Open `labs/lab07-context/lab07_cluster.ipynb` and run the setup cell.
4. **Part A** (guided practice):
   - A1: context versus prompt.
   - A2: few-shot examples and a sensitivity test (number, order, wording).
   - A3 (optional, not graded): breaking a task into a two-step chain.
   - A4: prompt versions scored on a small dev set with an LLM judge.
   - A5: an indirect prompt injection test with two defense layers.
5. **Part B** (applied lab), building the Co. app v1:
   - B1-B2: open `coapp/prompts.py` and complete the TODOs (system prompt, `format_chunk`, `build_messages`). Save, then rerun the reload cell.
   - B3: evaluate your app against a baseline on 20 gold questions, including 13 "trap" questions. Your first version's results are saved in `lab07_v1_results.json`, so later reruns keep them.
   - B4: add a rule for conflicting documents, bump `PROMPT_VERSION`, and measure trap accuracy again.
6. Answer the four **written analysis** questions with your own numbers, citing the chapter.
7. Complete the **AI-use reflection**.
8. Run the notebook top to bottom, check that `ck.report()` printed, and save.

If you get stuck on the Co. app, `coapp_reference/` is a complete working version. Lab 8 builds on the Co. app, so the reference is there to keep you moving. Write your own `prompts.py` first; your analysis should be about your prompt.

## What to submit

Upload to Canvas:
- `lab07_cluster.ipynb` **with outputs**
- `coapp/prompts.py`

## Grading

| Component | Points | How graded |
|---|---|---|
| Auto-checks | 50 | The grading script reads the `ck.report()` summary line and scales your check score to 50 |
| Written analysis | 40 | Uses your own results (15), correct concepts with chapter citation (15), clear reasoning and trade-offs (10) |
| AI-use reflection | 10 | Complete and specific (10), generic (5), missing (0) |

## Getting unstuck

- **Your edits to `prompts.py` don't show up:** save the file (Ctrl+S), then rerun the cell that calls `reload_coapp()`. If you see a `SyntaxError`, the traceback names the line in `prompts.py`.
- **"WARNING: prompts.py changed but PROMPT_VERSION is still ...":** bump `PROMPT_VERSION` whenever you change the prompt. That's the point of versioning, and it keeps your B3 and B4 numbers separate.
- **Trap questions still wrong after B4:** print the answer and its `sources`. Did the model cite the older document? Is the stale statement inside a document that is otherwise current? A date rule alone can't fix that case. Describe it in Q3.
- **Want to start Part B over with a clean slate:** delete `lab07_v1_results.json` (your saved first version) and `lab07_app_results.jsonl` (the cache), then rerun from B3. Deleting only `lab07_v1_results.json` makes B3 save your *current* prompt as the new first version.
- **The judge's verdict looks wrong:** judges make mistakes. Compare the answer with the reference yourself and mention it in your analysis. Don't change the judge to get a better score.
- **Anything else:** ask Copilot Chat about the exact error, and paste in the cell and the traceback.
