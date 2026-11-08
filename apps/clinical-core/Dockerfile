# Clinical Core API (FastAPI) — PR 1
# Multi-stage not needed for Python; slim image + non-root user (plan Fase 0.4).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY alembic ./alembic
COPY alembic.ini .

RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 4000

HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD curl -fsS http://localhost:4000/health || exit 1

# src/main.py exposes `app` and creates tables on startup (alembic 0001 exists too).
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "4000"]
