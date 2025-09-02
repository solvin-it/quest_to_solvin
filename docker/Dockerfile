FROM python:3.12-slim

# Fast, quiet, predictable Python in containers
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/src \
    # Streamlit sensible defaults for containers
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /src

# System deps (minimal) + curl for healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential gcc \
        libffi-dev libssl-dev \
        libjpeg-dev zlib1g-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Python deps (cached layer)
COPY requirements.txt /src/requirements.txt
RUN python -m pip install --upgrade pip wheel setuptools && \
    pip install -r /src/requirements.txt

# App code
COPY --chown=1000:1000 app/ /src/app/

# Defaults so the app works even without custom env
ENV LORE_PATH=/src/app/settings/lore.md \
    BACKGROUND_PATH=/src/app/settings/background.md \
    MODEL=""

# Non-root user for safety (uid/gid 1000 plays nice in most hosts)
RUN useradd --uid 1000 --create-home --shell /bin/bash appuser
USER appuser

EXPOSE 8501

# Healthcheck used by Compose/Cloud Run/K8s
HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8501/_stcore/health || exit 1

# Start the Streamlit app
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
