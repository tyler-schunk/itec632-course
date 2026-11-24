# Running the labs without Docker

Use this only if Docker Desktop won't run on your computer. It installs the same packages directly using `uv`, a fast Python installer.

1. Install uv: https://docs.astral.sh/uv/getting-started/installation/
2. Open a terminal **in this folder** and run:
   ```
   uv venv --python 3.14
   uv pip install -r image/requirements.txt
   uv pip install ./image
   ```
3. Copy `.env.example` to `.env` and paste in your two values (same as the main setup).
4. Connect to the KU VPN, then start JupyterLab:
   ```
   uv run jupyter lab
   ```
5. Run `00_setup_check.ipynb` the same way.

Next time, you only need step 4.
