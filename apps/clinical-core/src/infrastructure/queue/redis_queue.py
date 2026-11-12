from __future__ import annotations

import json
from uuid import UUID

import redis

from src.infrastructure.settings import settings


class RedisQueue:
    """Thin wrapper over the Redis document_jobs queue."""

    def __init__(self, client: redis.Redis | None = None) -> None:
        self._client = client or redis.Redis.from_url(settings.redis_url, decode_responses=True)

    def ping(self) -> bool:
        try:
            return bool(self._client.ping())
        except redis.RedisError:
            return False

    def push_analysis_job(self, *, document_id: UUID, extraction_run_id: UUID) -> None:
        payload = {
            "document_id": str(document_id),
            "extraction_run_id": str(extraction_run_id),
            "attempts": 0,
        }
        self._client.rpush(settings.redis_queue_name, json.dumps(payload))
