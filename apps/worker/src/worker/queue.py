from __future__ import annotations

import json

import redis

from .config import settings
from .schemas import DocumentJob


class RedisQueue:
    def __init__(self) -> None:
        self._client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

    def pop_job(self, timeout_seconds: int = 5) -> DocumentJob | None:
        item = self._client.blpop(settings.redis_queue_name, timeout=timeout_seconds)
        if item is None:
            return None

        _, raw_payload = item
        payload = json.loads(raw_payload)
        return DocumentJob.model_validate(payload)
