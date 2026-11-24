# Lab 04: Evaluation Methodology - perplexity, exact metrics, and AI judges

Chapter 3 of *AI Engineering* argues that evaluation is the hardest part of building with foundation models, and it gives you a toolbox: language-modeling metrics (cross-entropy, perplexity, bits-per-byte), exact evaluation against reference answers (exact match, lexical and semantic similarity), and AI as a judge, with its well-known biases. In this lab you use every tool in that box on Larkspur Ridge IT's help-desk questions. You compute perplexity by hand from a model's logits, score real model answers four different ways, and then test whether an LLM judge prefers its own family's answers or whichever answer it reads first. By the end you should know which metric to trust for which job, and why the help-desk assistant's evaluation can't rely on any single number.

## Where you'll work

| Notebook | Environment | Time |
|---|---|---|
| `lab04_colab.ipynb` | Google Colab, free **T4 GPU** (loads small Hugging Face models) | about 1.5-2 hours |
| `lab04_cluster.ipynb` | Your Docker JupyterLab on the **KU VPN** (course cluster) | about 2.5-3 hours |

Total: about 4-5 hours plus the Chapter 3 reading. The two notebooks are independent; do them in either order.

## Module objectives

| MO | Objective (Bloom level) | CO |
|---|---|---|
| MO 4.1 | **Compute** cross-entropy, perplexity, and bits-per-byte from a model's logits and **explain** how they depend on the text, the model, and the tokenizer (Bloom: Apply) | CO1, CO2 |
| MO 4.2 | **Implement** exact match, token F1, and embedding similarity, and **identify** answers where each one gives the wrong verdict (Bloom: Analyze) | CO2 |
| MO 4.3 | **Design** a scoring rubric and **use** an LLM as a judge with robust output parsing (Bloom: Create) | CO2 |
| MO 4.4 | **Measure** self-preference and position bias in LLM judges and their agreement with human labels (Bloom: Evaluate) | CO2 |
| MO 4.5 | **Recommend** an evaluation approach for the Larkspur help-desk assistant, justified with your own results and the chapter (Bloom: Evaluate) | CO2 |

## Steps

1. Read Chapter 3: "Challenges of Evaluating Foundation Models", "Understanding Language Modeling Metrics" (entropy through "Perplexity Interpretation and Use Cases"), "Exact Evaluation" (including "Similarity Measurements Against Reference Data" and "Introduction to Embedding"), "AI as a Judge" (including "How to Use AI as a Judge" and "Limitations of AI as a Judge"), and "Ranking Models with Comparative Evaluation". The analysis questions cite these sections.
2. **Colab:** open `lab04_colab.ipynb` in Colab (File > Open notebook > GitHub, or upload it), set the runtime to **T4 GPU**, and work through it top to bottom.
   - Part A: tokens and bytes, cross-entropy from logits, perplexity and bits-per-byte.
   - Part B: compare a Larkspur runbook, the same text shuffled, random characters, a public-domain book, and your own paragraph; compare four models (including one with a different tokenizer); measure how context lowers perplexity.
3. **Cluster:** with the VPN on, open `labs/lab04-eval-methods/lab04_cluster.ipynb` in your Docker JupyterLab.
   - Part A: build exact match, token F1, cosine similarity, and an LLM-judge rubric step by step.
   - Part B: get `qwen-small` answers to 25 gold questions (`corpus/larkspur-corpus/eval/`), score them four ways, run the judge-bias experiment with `qwen-moe` and `gemma-moe`, and **label 10 answers yourself** to see which metric agrees with you.
4. Answer the written analysis and AI-use reflection questions in **each** notebook.
5. Run the final `ck.report()` cell in each notebook and save.

## What to submit

Upload **both** notebooks to Canvas, with all outputs visible:
- `lab04_colab.ipynb` (download it from Colab: File > Download > Download .ipynb)
- `lab04_cluster.ipynb`

Canvas accepts multiple files in one submission.

## Grading

| Component | Points | How graded |
|---|---|---|
| Auto-checks (both notebooks, scaled) | 50 | Grading script reads the `ck.report()` line in each notebook |
| Written analysis | 40 | Uses your own results (15), correct concepts with chapter citation (15), clear reasoning and tradeoffs (10) |
| AI-use reflection | 10 | Complete and specific (10), generic (5), missing (0) |

## Getting unstuck

- **Colab says "CUDA not available" or is very slow:** Runtime > Change runtime type > T4 GPU, then Runtime > Restart and run all. If you hit "CUDA out of memory" in B2, restart the runtime and run all again; the notebook frees each model before loading the next.
- **Your cross-entropy doesn't match the Hugging Face loss:** remember the shift (logits at position *i* predict token *i+1*) and the minus sign. Print `token_nll[:5]` and `out.loss` side by side.
- **Judge scores come back as `None`:** print the raw judge reply. Usually the rubric lost its "Reply with JSON only" line, or a placeholder like `{answer}` was deleted. `parse_score()` already handles most messy outputs.
- **Rate-limit or timeout errors on the cluster:** just re-run the cell. Every reply is cached in `lab04_cache.json`, so finished requests are not sent again. Don't delete that file mid-lab.
- Ask Copilot Chat with the exact error message and the cell that produced it; then check its suggestion against the TODO hint before pasting.
