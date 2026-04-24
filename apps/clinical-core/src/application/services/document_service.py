from __future__ import annotations

from src.domain.entities.document import ClinicalDocument
from src.infrastructure.repositories.in_memory_document_repository import InMemoryDocumentRepository
from src.schemas.document import ClinicalDocumentCreateRequest


class DocumentService:
    """Application logic for clinical documents."""

    def __init__(self, repository: InMemoryDocumentRepository) -> None:
        self._repository = repository

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
        return self._repository.save(document)
