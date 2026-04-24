from __future__ import annotations

import logging

from .processor import DocumentProcessor
from .queue import RedisQueue

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def run() -> None:
    queue = RedisQueue()
    processor = DocumentProcessor()
    logger.info("Worker started. Waiting for jobs...")

    try:
        while True:
            job = queue.pop_job(timeout_seconds=5)
            if job is None:
                continue
            logger.info("Processing document_id=%s", job.document_id)
            processor.process(job)
    finally:
        processor.close()


if __name__ == "__main__":
    run()
