# Lab 01 - Foundation Models Under the Hood

Chapter 1 of *AI Engineering* explains what foundation models are, how they grew out of language models, and how AI engineering differs from traditional ML engineering. In this lab you do two things. First, you set up the tools you will use all semester: Docker, the KU VPN, and your personal key for the course AI cluster. Second, you load a real open-weight model (Qwen3-4B-Instruct-2507) onto a free Colab GPU and look under the hood: tokens, chat templates, model size, GPU memory, next-token probabilities, and why long conversations cost more. You finish by estimating, for Larkspur Ridge IT's help desk, how many tokens real messages and support chats use and what that means for cost and context limits.

## Where you'll work

| Part | Where | Time |
|---|---|---|
| Part 1: Setup check | Your computer: Docker JupyterLab on the KU VPN | 1-2 hours (first time; allow extra time if you have never installed Docker Desktop) |
| Part 2: `lab01_colab.ipynb` | Google Colab, free T4 GPU | about 3 hours |

## Module objectives

| MO | Objective (Bloom level) | CO |
|---|---|---|
| MO 1.1 | Explain how text is split into tokens and why token counts drive cost and context limits (Bloom: Understand) | CO1 |
| MO 1.2 | Describe how chat templates, next-token probabilities, and conversation history shape what an instruct model sees and produces (Bloom: Understand) | CO1 |
| MO 1.3 | Estimate a model's memory needs and the token cost of a support chat from its configuration and your measurements (Bloom: Apply) | CO1, CO4 |
| MO 1.4 | Evaluate whether a foundation-model application is worth building for a business, using Chapter 1's AI engineering stack and use-case evaluation ideas (Bloom: Evaluate) | CO1 |
| MO 1.5 | Configure and verify the course development environment (Docker, VPN, gateway key) (Bloom: Apply) | CO1 |

## Steps

**Reading:** Chapter 1, "The Rise of AI Engineering" (especially "From Language Models to Large Language Models"), "Foundation Model Use Cases" (skim), "Planning AI Applications", and "The AI Engineering Stack" (including "Three Layers of the AI Stack" and "AI Engineering Versus ML Engineering"). The analysis questions cite these sections.

### Part 1: Setup check (Docker + VPN + key)

1. Follow the course repository's `README.md` "One-time setup": install Docker Desktop, download the course folder, copy `.env.example` to `.env`, and paste in the two values from your key email.
2. Connect to the **KU VPN**, run `docker compose up` in the course folder, and open http://localhost:8888.
3. Open `notebooks/00_setup_check.ipynb` and choose **Run > Run All Cells**. Fix any red item by following the arrow under it, then run it again.
4. When every line is green, it prints **"ALL CHECKS PASSED. Setup code: XXXXXXXXXX"**. Copy that 10-character code. You will paste it in two places: the Colab notebook (Part 2) and your **Canvas submission comment**.
5. Try the "Your first request" cell at the bottom of the setup notebook. That is your first call to the course cluster.

### Part 2: Colab exploration

6. Open `labs/lab01-under-the-hood/lab01_colab.ipynb` in Google Colab (File > Upload notebook, or File > Open notebook > **GitHub** tab, paste the course repository's URL, and pick the notebook).
7. Select **Runtime > Change runtime type > T4 GPU**, then run the setup cells. Paste your setup code where asked.
8. Work through **Part A** (eight short steps). Each step has a small TODO and a self-check cell. Green means you got it.
9. Do **Part B**: the token report for help-desk messages, the 10-turn support chat cost estimate, and the context/KV-cache calculation.
10. Answer the five **written analysis** questions as you reach them in the notebook (Q1 after Step 7, Q2 after B.1, Q3 after B.3, Q4 and Q5 at the end), then the **AI-use reflection** at the bottom.
11. Run the last cell (`ck.report()`), then **File > Download > Download .ipynb**.

## What to submit

- `lab01_colab.ipynb` **with outputs** (download it from Colab after running the last cell).
- In the **Canvas submission comment**: your setup code from `00_setup_check.ipynb`.

## Grading

| Component | Points | How graded |
|---|---|---|
| Auto-checks (scaled from the `ck.report()` line) | 50 | Grading script |
| Written analysis | 40 | Uses your own results (15), correct concepts with chapter citation (15), clear reasoning and trade-offs (10) |
| AI-use reflection | 10 | Complete and specific (10), generic (5), missing (0) |

The setup code is part of the auto-checks. If your setup check cannot pass because of a VPN or Docker problem, email the instructor a screenshot before the deadline; you can still do the Colab part.

## Getting unstuck

- **"No GPU" / very slow generation:** you are on a CPU runtime. Runtime > Change runtime type > T4 GPU, then Runtime > Run all. Free GPUs are sometimes unavailable at busy times; try again later in the day.
- **Out of memory or "CUDA error":** Runtime > Restart session, then Run all. Do not load the model twice in one session.
- **`nan` or `inf` errors during generation:** switch to a smaller model in fp32: set `MODEL_ID = "Qwen/Qwen3-1.7B"` and `DTYPE = torch.float32` in the model-loading cell and re-run (the free T4 has no bfloat16 support). Your memory and speed numbers will then differ from the ones in the text; that is expected, so report what you get.
- **Setup check is red at "Can reach the gateway":** connect (or reconnect) the KU VPN, then restart Docker Desktop. The README's "Problems?" table covers the other common errors.
- Paste the exact error message into Copilot Chat and ask what it means. If you are still stuck after 20 minutes, post in the course Q&A discussion.
