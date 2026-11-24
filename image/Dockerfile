# ITEC 632 course image: JupyterLab + every package the cluster labs need.
# Built for both Intel/AMD (Windows, older Macs) and ARM (Apple Silicon) by the
# GitHub Actions workflow in .github/workflows/build-image.yml.
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends git curl sqlite3 \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Small course helper package: get_client(), MODELS, and the setup check.
COPY pyproject.toml /opt/itec632/pyproject.toml
COPY itec632 /opt/itec632/itec632
RUN pip install --no-deps /opt/itec632

# Run as a normal user, not root.
RUN useradd --create-home --uid 1000 student
USER student
WORKDIR /home/student/work

EXPOSE 8888
# No token/password: compose.yaml publishes the port on 127.0.0.1 only,
# so JupyterLab is reachable from the student's own machine and nowhere else.
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", \
     "--ServerApp.token=", "--ServerApp.password=", \
     "--ServerApp.root_dir=/home/student/work"]
