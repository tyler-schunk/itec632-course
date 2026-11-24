# ITEC 632 - Lab Environment

This folder is your lab workspace for the semester. It runs JupyterLab inside Docker, with everything preinstalled, so every student has the same setup.

Some labs run in **Google Colab** instead, when they need a GPU. Each lab tells you which one to use.

## One-time setup (about 20 minutes)

1. **Install Docker Desktop**: https://www.docker.com/products/docker-desktop/
   - On Windows, accept the WSL 2 option if it asks. If it says virtualization is disabled, see "Problems" below.
2. **Get this folder.** Click the green **Code** button on GitHub, choose **Download ZIP**, and unzip it somewhere easy to find, like Documents. (If you know git: `git clone` works too.)
3. **Add your key.** In the folder, copy `.env.example` to a new file named exactly `.env`. Open it in any text editor and paste in the two values from your key email.
   - Windows tip: in File Explorer, turn on View > Show > File name extensions so the file is really `.env`, not `.env.txt`.
4. **Connect to the KU VPN.** The AI cluster is only reachable on the KU network.
5. **Start the lab.** Open a terminal in this folder (Windows: right-click the folder > "Open in Terminal"; Mac: Terminal, then `cd` into the folder) and run:
   ```
   docker compose up
   ```
   The first run downloads the course image (a few minutes). Leave this window open while you work.
6. Open **http://localhost:8888** in your browser.
7. Open `notebooks/00_setup_check.ipynb` and run it (Run > Run All Cells). Everything should be green. Copy the **setup code** it prints into your Module 1 submission.

## Every time after that

Connect to the VPN, run `docker compose up` in this folder, and open http://localhost:8888. When you're done, press **Ctrl+C** in the terminal.

Everything you do is saved in this folder on your own computer (labs in `labs/`, the company documents in `corpus/`), so it's safe even if Docker is removed.

Labs marked **Colab** run in Google Colab instead; each lab's `LAB_GUIDE.md` tells you where to run each notebook.

## Problems?

| Symptom | Fix |
|---|---|
| "Can't reach the gateway" | Connect to (or reconnect) the KU VPN, then restart Docker Desktop. |
| "Key accepted" is red | Check `.env` for typos or extra spaces. The key starts with `sk-`. |
| Windows: "virtualization is disabled" | Turn on virtualization (Intel VT-x / AMD SVM) in your BIOS/UEFI settings, or use the no-Docker option below. Work laptops may block this. |
| Port 8888 already in use | Something else uses that port. Close other Jupyter windows, or change the first `8888` in `compose.yaml` to `8889` and open http://localhost:8889. |
| Anything else | Ask Copilot Chat with the exact error text, then email the instructor with a screenshot. |

If Docker won't run on your computer, see **FALLBACK_NO_DOCKER.md**.
