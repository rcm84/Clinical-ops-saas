from __future__ import annotations

from fastapi import APIRouter, status

from src.application.services.document_service import DocumentService
from src.infrastructure.repositories.in_memory_document_repository import InMemoryDocumentRepository
from src.schemas.document import ClinicalDocumentCreateRequest, ClinicalDocumentResponse
from src.schemas.health import HealthResponse

router = APIRouter()
_repository = InMemoryDocumentRepository()
_document_service = DocumentService(repository=_repository)


@router.get("/health", response_model=HealthResponse, tags=["health"])
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post(
    "/documents",
    response_model=ClinicalDocumentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["documents"],
)
def create_document(payload: ClinicalDocumentCreateRequest) -> ClinicalDocumentResponse:
    document = _document_service.create_document(payload)
    return ClinicalDocumentResponse.model_validate(document)
