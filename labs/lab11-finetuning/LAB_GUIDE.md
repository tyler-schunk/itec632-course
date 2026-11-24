# Lab 11 - Finetuning in Practice

Fine-tuning is the most expensive way to adapt a model, so an AI engineer should know when it pays off and what it costs. In this lab you fine-tune **Qwen3-1.7B** with **LoRA** on the Larkspur dataset you built in Lab 10, on a **free Colab T4 GPU**. You start with the memory math that explains why full fine-tuning doesn't fit on a 15 GB GPU but LoRA does, choose LoRA hyperparameters, and watch the loss. Then you run the real fine-tune and compare base vs fine-tuned answers on your held-out test set, separately for document facts and for the format of resolution notes, and weigh fine-tuning against your Lab 8 RAG pipeline. This lab covers **Chapter 7** of *AI Engineering*: memory bottlenecks and memory math, parameter-efficient fine-tuning and LoRA, model merging, and fine-tuning vs RAG.

## Where you'll work

- **Colab notebook:** `lab11_colab.ipynb` on Google Colab with a **T4 GPU** (Runtime > Change runtime type > T4 GPU). No cluster or VPN needed.
- **Time:** about 3-4 hours, including about 25-35 minutes of GPU time. Do it in one sitting if you can: Colab deletes files when the session ends.
- **Data:** your `larkspur_sft_train.jsonl` and `larkspur_sft_test.jsonl` from Lab 10 (`my_dataset/`). If you don't have them, the notebook uses the fallback dataset automatically.

## Module objectives

| MO | Objective | CO |
|---|---|---|
| MO 11.1 | **Calculate** the memory needed for full fine-tuning vs LoRA from parameter counts and optimizer states (Bloom: Apply) | CO4 |
| MO 11.2 | **Configure** and run a 16-bit LoRA fine-tune (rank, alpha, target modules) within a free GPU's limits (Bloom: Apply) | CO4 |
| MO 11.3 | **Evaluate** a fine-tuned model against its base model with reference-based metrics and manual inspection (Bloom: Evaluate) | CO2, CO4 |
| MO 11.4 | **Justify** when to fine-tune vs use RAG, using your own results and the chapter's criteria (Bloom: Evaluate) | CO3, CO4 |

## Steps

1. Read Chapter 7 (Finetuning Overview, When to Finetune, Memory Bottlenecks, Finetuning Techniques).
2. Open `lab11_colab.ipynb` in Colab (File > Upload notebook, or open it from the course GitHub repo). Select a **T4 GPU** runtime.
3. Run the install cell. If Colab asks you to restart the session, do it, then continue from the next cell.
4. Upload your two Lab 10 JSONL files with the Files panel (folder icon on the left). Skip this to use the fallback dataset.
5. **Part A (guided):**
   - A1: compute inference and full fine-tuning memory for the model.
   - A2: write the `LoraConfig` and see how few parameters it trains.
   - A3: run 15 training steps and watch the loss.
6. **Part B (applied):**
   - B1: record base-model answers on the 40 test examples.
   - B2: fine-tune for 2 epochs and record runtime and peak GPU memory.
   - B3: compute ROUGE-L and token F1 (you write `token_f1`), and judge 5 examples yourself.
   - B4: optionally paste your Lab 8 RAG correctness number.
   - B5: save the adapter, compare its size with the model, and merge it.
7. Answer the four written-analysis questions and the AI-use reflection, run the final cell.
8. **File > Download > Download .ipynb**, then upload that file to Canvas.

## What to submit

- `lab11_colab.ipynb` **with outputs** (downloaded from Colab), uploaded to Canvas.
- The adapter itself is not submitted (download it with the optional cell if you want to keep it).

## Grading

| Component | Points | How graded |
|---|---|---|
| Auto-checks (23 check points scaled to 50) | 50 | Grading script reads the `ck.report()` line |
| Written analysis | 40 | Uses your own results (15), correct concepts with chapter citation (15), clear reasoning and tradeoffs (10) |
| AI-use reflection | 10 | Complete and specific (10), generic (5), missing (0) |

## Getting unstuck

- **"CUDA out of memory".** Restart the session (Runtime > Restart session) and run again from the top: an earlier run may still hold memory. If it happens again, change `per_device_train_batch_size` to 2 and `gradient_accumulation_steps` to 4 in `sft_args` (same effective batch, less memory), and mention it in Q1.
- **Loss is `nan` or `0.0` from the first step.** That's an fp16 numerical problem. Set `DTYPE = torch.float32` in the setup cell (keep `USE_FP16 = True`), restart, and re-run; training gets slower but stable. Mention it in your analysis.
- **The install cell shows dependency warnings.** Warnings are fine; errors are not. If an import fails after the install, restart the session and run the import cell again.
- **Colab disconnected mid-run.** Free Colab sessions time out when idle. Keep the tab open and visible during the training cells; if you lose the session, start again from the top (about 25 minutes of GPU time).
- Ask Copilot Chat with the exact error message, and include the library versions printed by the setup cell. AI assistants often suggest old argument names (for example `max_seq_length`, `torch_dtype` or `warmup_ratio`); this notebook uses the current ones (`max_length`, `dtype`, `warmup_steps`).
