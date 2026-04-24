from __future__ import annotations

from uuid import UUID

from .db import ClinicalDocumentModel, ExtractionRunModel, SessionLocal
from .openmed import OpenMedClient
from .schemas import DocumentJob


class DocumentProcessor:
    def __init__(self) -> None:
        self._openmed = OpenMedClient()

    def close(self) -> None:
        self._openmed.close()

    def process(self, job: DocumentJob) -> None:
        with SessionLocal() as session:
            document = session.get(ClinicalDocumentModel, UUID(job.document_id))
            if document is None:
                return

            document.status = "processing"
            session.flush()

            try:
                openmed_result = self._openmed.analyze_text(
                    text=document.raw_text,
                    language=document.language,
                )
                run = ExtractionRunModel(
                    document_id=document.id,
                    engine="openmed",
                    engine_version="v1",
                    status="completed",
                    raw_output_json=openmed_result,
                )
                session.add(run)
                document.status = "processed"
            except Exception as exc:  # noqa: BLE001
                run = ExtractionRunModel(
                    document_id=document.id,
                    engine="openmed",
                    engine_version="v1",
                    status="failed",
                    raw_output_json={"error": str(exc)},
                )
                session.add(run)
                document.status = "failed"

            session.commit()
