# Lab 09 - Agents and Tool Use

Retrieval (Lab 8) helps when the answer is written down somewhere. A lot of what Larkspur's service desk asks is not in any document: it lives in Harbor PSA data. "Which open tickets does Kaw Valley Auto Group have, and what's our response target?" needs a lookup, a second lookup, and some reasoning about the results. In this lab you turn the model into an **agent**: you give it tools over the Larkspur ticket database, write the loop that lets it plan, call tools and read the results, and then measure how well (and how efficiently) it works. This lab covers the "Agents" part of **Chapter 6** of *AI Engineering*: tools, planning with function calling, write actions, and agent failure modes and evaluation.

## Where you'll work

- **Cluster notebook:** `lab09_cluster.ipynb` in your local Docker JupyterLab, with the **KU VPN** on.
- **Time:** about 3 hours. This is a **Part-A-only week** (side project 2 is due), so Part B is an optional bonus.
- **Cluster use:** about 150 requests. The notebook paces itself; you don't need to do anything.

## Module objectives

| MO | Objective | CO |
|---|---|---|
| MO 9.1 | **Implement** read-only, parameterized tools and their JSON schemas, and use native tool calling with the OpenAI tools API (Bloom: Apply) | CO3 |
| MO 9.2 | **Construct** an agent loop with a step limit, argument validation, and error messages the model can recover from (Bloom: Create) | CO3 |
| MO 9.3 | **Evaluate** an agent on tasks with known answers, measuring success, steps and tokens per task (Bloom: Evaluate) | CO2, CO3 |
| MO 9.4 | **Analyze** agent failures as planning failures, tool failures, or efficiency problems, and compare tool-calling ability across models (Bloom: Analyze) | CO3, CO4 |
| MO 9.5 | **Explain** why write actions need human confirmation, using a simulated confirmation gate (Bloom: Understand) | CO5 |

## Steps

1. Read Chapter 6, the "Agents" section: "Agent Overview", "Tools" (including "Write actions"), "Planning" (especially "Plan generation" with its "Function calling" subsection, "Reflection and error correction", and "Tool selection"), and "Agent Failure Modes and Evaluation" ("Planning failures", "Tool failures", "Efficiency"). Skim "Memory".
2. Open `labs/lab09-agents/lab09_cluster.ipynb`. Run **Run > Run All Cells** once: everything runs, and the red checks show what's left.
3. **Part A (graded):** work through A1-A8 in order. Each section has a short TODO followed by a check cell.
   - A1: write `get_client` and `sla_target` (parameterized SQL on a read-only connection).
   - A2: write the `sla_target` tool schema; see a native tool call.
   - A3: add argument validation that returns errors to the model.
   - A4: write the body of the agent loop.
   - A5: write the confirmation gate for the simulated "write" tool.
   - A6: write the answer scorer and evaluate the agent on 15 tasks.
   - A7: read the traces and label failures (planning / tool misuse / tool failure / efficiency).
   - A8: compare `qwen-moe`, `gemma-moe` and `qwen-small` on 5 tasks.
4. **Part B (optional bonus, up to 10 points):** build Co. app v3. Copy your Lab 8 Co. app into `coapp/`, add `tools.py`, and add a router to `assistant.answer()`. A complete reference v3 is in `coapp_reference/` if you get stuck (Lab 14 builds on v3, so having a working copy matters).
5. Answer the four written-analysis questions using your own numbers and traces, with chapter citations.
6. Complete the AI-use reflection, run the final cell, save.

## What to submit

- `lab09_cluster.ipynb` **with outputs**, uploaded to Canvas. The last cell must show the self-check summary.
- If you did Part B, nothing extra to upload: the bonus checks run inside the notebook.

## Grading

| Component | Points | How graded |
|---|---|---|
| Auto-checks (Part A, 30 check points scaled to 50) | 50 | Grading script reads the `ck.report()` line |
| Written analysis | 40 | Uses your own results (15), correct concepts with chapter citation (15), clear reasoning and tradeoffs (10) |
| AI-use reflection | 10 | Complete and specific (10), generic (5), missing (0) |
| **Part B bonus** | up to +10 | Bonus auto-checks, shown as `partB_bonus_points` in the summary |

## Getting unstuck

- **The agent loops until max_steps or repeats the same call.** Print the trace (`show_trace("T04")`). Usually a tool message is missing its `tool_call_id`, or you appended the tool result but not the assistant turn with its `tool_calls` first. The order must be: assistant turn, then one tool message per call.
- **"No client with code ..." or a pattern error.** That's the validation working: the model passed a name where a code was needed. Good agents recover by calling `get_client` first. If yours doesn't, read the error message it got: is it clear enough to act on?
- **A task "fails" but the answer looks right.** Look at `must_include` for that task. The scorer needs every fact (for example both the ticket ID *and* the SLA target). Don't change the tasks; explain the case in your analysis.
- **Rate-limit errors (429).** Wait a minute and re-run the cell. Don't lower `PACE_S` below 1.0.
- Ask Copilot Chat with the exact error message and the cell that produced it. For agent bugs, paste the trace too.
