# Lab 02 - Model Architecture, Size, and Memory

Chapter 2 of *AI Engineering* explains how a foundation model's training data, architecture, and size shape what it can do and what it costs to run. In this lab you read the real configuration files of the four course models (a dense 27B model, two mixture-of-experts models, and a small 4B model), work out by hand how much memory each one needs for its weights and its KV cache, use that to size a server for Larkspur's help desk, and then measure how fast three of them generate text on the course cluster. You will see why a 35B mixture-of-experts model can be faster than a 27B dense one, and use that to make a deployment recommendation for Larkspur Ridge IT's help-desk assistant. This is also your first lab that calls the cluster from your own code.

**Where you'd use this at work:** When someone asks "can we run this model on our own server?", memory math answers it. You size memory for the weights plus the KV cache and pick hardware, much like sizing a VM.

## Where you'll work

| Notebook | Where | Time |
|---|---|---|
| `lab02_cluster.ipynb` | Your Docker JupyterLab, on the KU VPN | about 3-3.5 hours |

## Module objectives

| MO | Objective (Bloom level) | CO |
|---|---|---|
| MO 2.1 | Interpret a model's configuration file to identify its architecture choices (dense vs mixture of experts, attention layer types) (Bloom: Understand) | CO1 |
| MO 2.2 | Calculate weight memory at different precisions and KV-cache memory for real models, and use them to size hardware (Bloom: Apply) | CO1, CO4 |
| MO 2.3 | Measure generation latency and output tokens per second of dense and MoE models through an API (Bloom: Apply) | CO4 |
| MO 2.4 | Analyze how active parameters, memory bandwidth, and scaling laws explain the speed, memory, and cost trade-offs between models (Bloom: Analyze) | CO1, CO4 |

## Steps

**Reading:** Chapter 2, "Training Data" and "Modeling": "Model Architecture" (including "Transformer architecture" and "Other model architectures") and "Model Size" (including "Scaling law: Building compute-optimal models" and "Scaling bottlenecks"). The analysis questions cite these sections. ("Post-Training" and "Sampling" are next week.)

1. Connect to the **KU VPN**, run `docker compose up` in your course folder, and open http://localhost:8888.
2. Open `labs/lab02-model-size/lab02_cluster.ipynb`. (Open it from this folder: it uses the `model_configs/` snapshot next to it if Hugging Face cannot be reached.)
3. Run the **Setup** cell and confirm the green check.
4. **Part A:** download the model configs and read the config table (dense or mixture of experts? how many experts?). A provided cell counts each model's total and active parameters for you. Then complete the short TODOs: the active fraction, `weight_gb` (weight memory at 16, 8, and 4 bits), `kv_bytes_per_token` (KV-cache memory), and a server-sizing step (`memory_needed_gb`, whether 20 help-desk chats fit on one Mac Studio, and the most chats that would fit). Before two of the tables you write down a quick prediction; any honest guess earns the point. Each step has a check cell.
5. **Part B:** finish `measure()`, run the speed experiment (33 requests, about 3-6 minutes), then build the summary table and speedup.
6. Answer the five **written analysis** questions and the **AI-use reflection**.
7. Run the last cell (`ck.report()`), save the notebook (File > Save), and upload the .ipynb.

## What to submit

- `lab02_cluster.ipynb` **with outputs**.

## Grading

| Component | Points | How graded |
|---|---|---|
| Auto-checks (scaled from the `ck.report()` line) | 50 | Grading script |
| Written analysis | 40 | Uses your own results (15), correct concepts with chapter citation (15), clear reasoning and trade-offs (10) |
| AI-use reflection | 10 | Complete and specific (10), generic (5), missing (0) |

## Getting unstuck

- **Memory numbers look 1,000x too big or too small (or a table says "Complete the TODOs"):** check your units. `weight_gb` gets parameters in *billions* and must return decimal GB (1 GB = 1e9 bytes, not 1024**3); 16 bits is 2 bytes. Test it on the docstring example (`weight_gb(7, 16)` should be 14.0), then re-run the table cells below it in order.
- **Speeds vary a lot between runs:** that is real. Other students share the cluster, so use the median (the notebook does) and mention the variation in your analysis. If one model looks far slower than expected, re-run the experiment cell at a quieter time.
- **`RateLimitError` or 429:** you are sending too fast (the limit is 60 requests per minute). Wait a minute and re-run; do not remove the `time.sleep` in the loop.
- **"Download failed ... model_configs missing":** you opened the notebook from a different folder. Open it from `labs/lab02-model-size/`.
- Paste the exact error into Copilot Chat. Ask it to explain your memory math too, but check its numbers against the config: assistants often quote parameter counts from memory.
