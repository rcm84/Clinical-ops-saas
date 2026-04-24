from __future__ import annotations

from src.domain.entities.document import ClinicalDocument
from src.infrastructure.repositories.in_memory_document_repository import InMemoryDocumentRepository
from src.schemas.document import DocumentCreateRequest


class DocumentService:
    """Application logic for clinical documents."""

    def __init__(self, repository: InMemoryDocumentRepository) -> None:
        self._repository = repository

    def create_document(self, request: DocumentCreateRequest) -> ClinicalDocument:
        document = ClinicalDocument(
            patient_id=request.patient_id,
            title=request.title,
            document_type=request.document_type,
            created_by=request.created_by,
        )
        return self._repository.save(document)
