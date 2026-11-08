from __future__ import annotations

import logging
import time

from .config import settings
from .logging_config import configure_json_logging
from .processor import DocumentProcessor, TransientProcessingError
from .queue import RedisQueue
from .schemas import DocumentJob

logger = logging.getLogger(__name__)


def _backoff_seconds(attempts: int) -> float:
    """Exponential backoff: base * 2^(attempts-1), capped at the configured max."""
    delay = settings.retry_base_delay_seconds * (2 ** max(attempts - 1, 0))
    return min(delay, settings.retry_max_delay_seconds)


def run() -> None:
    configure_json_logging()
    queue = RedisQueue()
    processor = DocumentProcessor()
    logger.info(
        "worker started",
        extra={"queue": settings.redis_queue_name, "dlq": settings.redis_dlq_name},
    )

    try:
        while True:
            job = queue.pop_job(timeout_seconds=5)
            if job is None:
                continue
            context = {"document_id": job.document_id, "attempts": job.attempts}
            try:
                processor.process(job)
            except LookupError as exc:
                # Permanent: the document does not exist, retrying cannot help.
                queue.push_dlq(job, reason=str(exc))
                logger.error("job discarded to DLQ (document not found)", extra=context)
            except TransientProcessingError as exc:
                if job.attempts + 1 >= settings.max_attempts:
                    processor.fail_job(job, str(exc))
                    queue.push_dlq(job, reason=str(exc))
                    logger.error(
                        "job exhausted retries, sent to DLQ",
                        extra={**context, "error": str(exc)},
                    )
                else:
                    job.attempts += 1
                    delay = _backoff_seconds(job.attempts)
                    logger.warning(
                        "job failed, retrying",
                        extra={**context, "error": str(exc), "retry_in_seconds": delay},
                    )
                    # NOTE: the worker sleeps during backoff (single-threaded loop).
                    # A delayed-retry queue would avoid blocking; follow-up if needed.
                    time.sleep(delay)
                    queue.push_job(job)
            except Exception as exc:  # noqa: BLE001 - never kill the loop on unexpected errors
                logger.exception(
                    "unexpected error processing job",
                    extra={**context, "error": str(exc)},
                )
                queue.push_dlq(job, reason=f"unexpected: {exc}")
    finally:
        processor.close()


if __name__ == "__main__":
    run()
