from __future__ import annotations

import logging
from uuid import UUID

from sqlalchemy.orm import Session

from .config import settings
from .db import ClinicalDocumentModel, ExtractionRunModel, SessionLocal
from .openmed import OpenMedClient
from .schemas import DocumentJob

logger = logging.getLogger(__name__)


class TransientProcessingError(Exception):
    """Retryable failure (OpenMed / network). Raised so the main loop can retry."""


class DocumentProcessor:
    def __init__(self) -> None:
        self._openmed = OpenMedClient()

    def close(self) -> None:
        self._openmed.close()

    def process(self, job: DocumentJob) -> None:
        """Process one job.

        Raises LookupError when the document does not exist (permanent) and
        TransientProcessingError on retryable failures. On success the
        extraction run created by clinical-core is completed and the document
        is marked as processed.
        """
        with SessionLocal() as session:
            document = session.get(ClinicalDocumentModel, UUID(job.document_id))
            if document is None:
                raise LookupError(f"document not found: {job.document_id}")

            run = self._load_or_create_run(session, job, document)
            document.status = "processing"
            session.commit()

            try:
                openmed_result = self._openmed.analyze_text(
                    text=document.raw_text,
                    language=document.language,
                )
            except Exception as exc:
                raise TransientProcessingError(str(exc)) from exc

            run.status = "completed"
            run.raw_output_json = openmed_result
            document.status = "processed"
            session.commit()
            logger.info(
                "document processed",
                extra={"document_id": job.document_id, "extraction_run_id": str(run.id)},
            )

    def fail_job(self, job: DocumentJob, error: str) -> None:
        """Final failure (retries exhausted): mark document and run as failed."""
        with SessionLocal() as session:
            document = session.get(ClinicalDocumentModel, UUID(job.document_id))
            if document is None:
                return
            run = self._load_or_create_run(session, job, document)
            run.status = "failed"
            run.raw_output_json = {"error": error}
            document.status = "failed"
            session.commit()

    def _load_or_create_run(
        self, session: Session, job: DocumentJob, document: ClinicalDocumentModel
    ) -> ExtractionRunModel:
        if job.extraction_run_id:
            run = session.get(ExtractionRunModel, UUID(job.extraction_run_id))
            if run is not None:
                return run
        run = ExtractionRunModel(
            document_id=document.id,
            engine="openmed",
            engine_version=settings.openmed_version,
            status="processing",
            raw_output_json={},
        )
        session.add(run)
        session.flush()
        return run
