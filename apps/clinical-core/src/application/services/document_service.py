from __future__ import annotations

from src.domain.entities.extraction_run import ExtractionRun
from src.domain.entities.document import ClinicalDocument
from src.infrastructure.repositories.sqlalchemy_document_repository import SQLAlchemyDocumentRepository
from src.infrastructure.repositories.sqlalchemy_extraction_run_repository import SQLAlchemyExtractionRunRepository
from src.schemas.document import ClinicalDocumentAnalyzeRequest, ClinicalDocumentCreateRequest


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

    def analyze_document(self, request: ClinicalDocumentAnalyzeRequest) -> tuple[ClinicalDocument, ExtractionRun]:
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
