from __future__ import annotations

import os


class AppSettings:
    """Runtime settings for clinical-core (Redis queue + OpenMed)."""

    def __init__(self) -> None:
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis_queue_name = os.getenv("REDIS_QUEUE_NAME", "document_jobs")
        self.redis_dlq_name = os.getenv("REDIS_DLQ_NAME", "document_jobs_dlq")
        self.openmed_base_url = os.getenv("OPENMED_BASE_URL", "http://localhost:8080")
        self.openmed_timeout_seconds = float(os.getenv("OPENMED_TIMEOUT_SECONDS", "5"))


settings = AppSettings()
