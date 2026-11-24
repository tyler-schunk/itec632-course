# Lab 15 - the Larkspur Co. app service with router, traces and feedback.
# Same image recipe as Lab 14; traces go to /app/logs (mounted from ./logs).
#
# Each instruction below creates an image LAYER. Docker caches layers, so we copy
# requirements.txt and install packages BEFORE copying our code: editing app/*.py
# then only rebuilds the last small layers, not the slow pip install.
#
# Secrets are NOT in this file. The gateway URL and key arrive at RUN time from
# your .env file (see compose.yaml), so the image itself contains no key.

# 1. Small official Python base image (same Python as the course image).
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 2. Dependencies first (pinned versions) - this layer is reused until requirements.txt changes.
COPY requirements.txt .
RUN pip install -r requirements.txt

# 3. Our code: the Co. app package and the web service around it.
COPY coapp/ ./coapp/
COPY app/ ./app/

# 4. Run as a normal user, not root. /app/cache holds the embedding cache, /app/logs the traces.
RUN useradd --create-home --uid 1000 appuser \
 && mkdir -p /app/cache /app/logs \
 && chown appuser:appuser /app/cache /app/logs
USER appuser

# 5. Non-secret settings. The corpus is mounted read-only at /corpus by compose.yaml.
ENV ITEC632_CORPUS=/corpus \
    COAPP_CACHE_DIR=/app/cache \
    COAPP_LOG_DIR=/app/logs

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4)" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
