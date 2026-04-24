from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/clinical_core",
    )
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis_queue_name: str = os.getenv("REDIS_QUEUE_NAME", "document_jobs")
    openmed_base_url: str = os.getenv("OPENMED_BASE_URL", "http://localhost:8081")
    openmed_analyze_path: str = os.getenv("OPENMED_ANALYZE_PATH", "/analyze-text")
    openmed_timeout_seconds: float = float(os.getenv("OPENMED_TIMEOUT_SECONDS", "30"))


settings = Settings()
