from __future__ import annotations

from uuid import UUID

from src.domain.entities.extraction_run import ExtractionRun
from src.domain.entities.document import ClinicalDocument
from src.infrastructure.repositories.sqlalchemy_document_repository import SQLAlchemyDocumentRepository
from src.infrastructure.repositories.sqlalchemy_extraction_run_repository import SQLAlchemyExtractionRunRepository
from src.schemas.document import (
    ClinicalDocumentAnalyzeRequest,
    ClinicalDocumentCreateRequest,
    ProcessingStatus,
)

# Engine version pinned to the OpenMed image used in docker-compose (PR 1).
OPENMED_ENGINE = "openmed"
OPENMED_ENGINE_VERSION = "3.1.0"


class DocumentService:
    """Application logic for clinical documents."""

    def __init__(
        self,
        document_repository: SQLAlchemyDocumentRepository,
        extraction_run_repository: SQLAlchemyExtractionRunRepository,
    ) -> None:
        self._document_repository = document_repository
        self._extraction_run_repository = extraction_run_repository

    def create_document(self, request: ClinicalDocumentCreateRequest) -> ClinicalDocument:
        document = ClinicalDocument(
            organization_id=request.organization_id,
            patient_external_id=request.patient_external_id,
            source_type=request.source_type,
            document_type=request.document_type,
            language=request.language,
            raw_text=request.raw_text,
            status=request.status,
        )
        return self._document_repository.save(document)

    def get_document(self, document_id: UUID) -> ClinicalDocument | None:
        return self._document_repository.get_by_id(document_id)

    def list_extraction_runs(self, document_id: UUID) -> list[ExtractionRun]:
        return self._extraction_run_repository.get_by_document_id(document_id)

    def prepare_analysis(
        self, document_id: UUID
    ) -> tuple[ClinicalDocument, ExtractionRun] | None:
        """Create a queued extraction run and mark the document as processing.

        The router commits this and then pushes the job to Redis; the worker
        picks it up, calls OpenMed and completes the run (see apps/worker).
        Returns None when the document does not exist.
        """
        document = self._document_repository.get_by_id(document_id)
        if document is None:
            return None
        extraction_run = ExtractionRun(
            document_id=document.id,
            engine=OPENMED_ENGINE,
            engine_version=OPENMED_ENGINE_VERSION,
            status="queued",
            raw_output_json={},
        )
        saved_run = self._extraction_run_repository.save(extraction_run)
        self._document_repository.update_status(document.id, ProcessingStatus.PROCESSING)
        document.status = ProcessingStatus.PROCESSING
        return document, saved_run

    def analyze_document(self, request: ClinicalDocumentAnalyzeRequest) -> tuple[ClinicalDocument, ExtractionRun]:
        """Legacy synchronous analyze: the caller provides the extraction output.

        Kept for compatibility; the async flow is POST /documents/{id}/analyze.
        """
        document = self.create_document(request)
        extraction_run = ExtractionRun(
            document_id=document.id,
            engine=request.extraction.engine,
            engine_version=request.extraction.engine_version,
            status=request.extraction.status,
            raw_output_json=request.extraction.raw_output_json,
        )
        saved_run = self._extraction_run_repository.save(extraction_run)
        return document, saved_run
