# ITEC 632 Labs

One lab per module. Each lab folder has a `LAB_GUIDE.md` (the same text as the Canvas assignment) and the notebook(s) you submit. Read the guide first: it says which chapter sections to read, where each notebook runs, and how the lab is graded.

**Where labs run**
- **Cluster:** your Docker JupyterLab (`docker compose up` in the top folder, then http://localhost:8888), with the **KU VPN** on. These notebooks call the course models.
- **Colab:** Google Colab with a free **T4 GPU** (Runtime > Change runtime type > T4 GPU). Upload the notebook to Colab or open it from GitHub. Colab can't reach the course cluster and doesn't need to.
- Labs 14 and 15 also need a terminal on **your own computer** to run `docker compose up --build` inside the lab folder.

| Lab | Title | Module / week | Reading | Environment | Notebook(s) | Folder |
|---|---|---|---|---|---|---|
| 01 | Foundation Models Under the Hood | 1 | Ch. 1 | Both (setup check on the cluster, then Colab) | `notebooks/00_setup_check.ipynb`, `lab01_colab.ipynb` | [lab01-under-the-hood](lab01-under-the-hood/) |
| 02 | Model Architecture, Size, and Memory | 2 | Ch. 2 | Cluster | `lab02_cluster.ipynb` | [lab02-model-size](lab02-model-size/) |
| 03 | Post-Training and Sampling | 3 | Ch. 2 | Both | `lab03_colab.ipynb`, `lab03_cluster.ipynb` | [lab03-sampling](lab03-sampling/) |
| 04 | Evaluation Methodology | 4 | Ch. 3 | Both | `lab04_colab.ipynb`, `lab04_cluster.ipynb` | [lab04-eval-methods](lab04-eval-methods/) |
| 05 | Evaluate AI Systems and Choose a Model (Part A only) | 5 | Ch. 4 | Cluster | `lab05_cluster.ipynb` | [lab05-model-selection](lab05-model-selection/) |
| 06 | Prompt Engineering Fundamentals | 6 | Ch. 5 | Cluster | `lab06_cluster.ipynb` | [lab06-prompting](lab06-prompting/) |
| 07 | Context Construction and Prompt Iteration (Co. app v1) | 7 | Ch. 5 | Cluster | `lab07_cluster.ipynb` | [lab07-context](lab07-context/) |
| 08 | Retrieval-Augmented Generation (Co. app v2) | 8 | Ch. 6 | Cluster | `lab08_cluster.ipynb` | [lab08-rag](lab08-rag/) |
| 09 | Agents and Tool Use (Co. app v3, Part A only) | 9 | Ch. 6 | Cluster | `lab09_cluster.ipynb` | [lab09-agents](lab09-agents/) |
| 10 | Dataset Engineering | 10 | Ch. 7 + Ch. 8 | Cluster | `lab10_cluster.ipynb` | [lab10-dataset-engineering](lab10-dataset-engineering/) |
| 11 | Finetuning in Practice | 11 | Ch. 7 | Colab | `lab11_colab.ipynb` | [lab11-finetuning](lab11-finetuning/) |
| 12 | Inference Performance Metrics on Real Hardware | 12 | Ch. 9 | Cluster | `lab12_cluster.ipynb` | [lab12-inference-metrics](lab12-inference-metrics/) |
| 13 | Inference Service Optimization (Part A only) | 13 | Ch. 9 | Cluster | `lab13_cluster.ipynb` | [lab13-serving-optimization](lab13-serving-optimization/) |
| 14 | Deploying the Assistant | 14 | Ch. 10 | Cluster + Docker on your computer | `lab14_cluster.ipynb` | [lab14-deploy](lab14-deploy/) |
| 15 | Monitoring, Routing, and User Feedback | 15 | Ch. 10 | Cluster + Docker on your computer | `lab15_cluster.ipynb` | [lab15-observability](lab15-observability/) |

"Part A only" weeks (5, 9, 13) are side-project weeks: Part A is graded and Part B is an optional bonus.

**Submitting:** run the last cell (`ck.report()`), save, and upload the `.ipynb` file(s) **with outputs** to Canvas. Colab: File > Download > Download .ipynb.
