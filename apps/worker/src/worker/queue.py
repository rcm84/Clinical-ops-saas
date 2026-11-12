from __future__ import annotations

import json
import logging

import redis

from .config import settings
from .schemas import DocumentJob

logger = logging.getLogger(__name__)


class RedisQueue:
    def __init__(self) -> None:
        self._client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

    def push_job(self, job: DocumentJob) -> None:
        self._client.rpush(settings.redis_queue_name, job.model_dump_json())

    def push_dlq(self, job: DocumentJob, *, reason: str) -> None:
        payload = json.loads(job.model_dump_json())
        payload["dlq_reason"] = reason
        self._client.rpush(settings.redis_dlq_name, json.dumps(payload))

    def pop_job(self, timeout_seconds: int = 5) -> DocumentJob | None:
        item = self._client.blpop(settings.redis_queue_name, timeout=timeout_seconds)
        if item is None:
            return None

        _, raw_payload = item
        try:
            return DocumentJob.model_validate_json(raw_payload)
        except (ValueError, TypeError) as exc:
            # Poison payload: never retry, keep a copy in the DLQ for inspection.
            logger.error(
                "invalid job payload, sent to DLQ",
                extra={"raw_payload": raw_payload, "error": str(exc)},
            )
            self._client.rpush(settings.redis_dlq_name, raw_payload)
            return None
