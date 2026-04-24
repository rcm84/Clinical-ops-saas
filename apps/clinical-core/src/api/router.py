from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.application.services.document_service import DocumentService
from src.infrastructure.db.session import get_db
from src.infrastructure.repositories.sqlalchemy_document_repository import SQLAlchemyDocumentRepository
from src.infrastructure.repositories.sqlalchemy_extraction_run_repository import SQLAlchemyExtractionRunRepository
from src.schemas.document import (
    ClinicalDocumentAnalyzeRequest,
    ClinicalDocumentAnalyzeResponse,
    ClinicalDocumentCreateRequest,
    ClinicalDocumentResponse,
    ExtractionRunResponse,
)
from src.schemas.health import HealthResponse

router = APIRouter()


def get_document_service(db: Session = Depends(get_db)) -> DocumentService:
    return DocumentService(
        document_repository=SQLAlchemyDocumentRepository(session=db),
        extraction_run_repository=SQLAlchemyExtractionRunRepository(session=db),
    )


@router.get("/health", response_model=HealthResponse, tags=["health"])
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post(
    "/documents",
    response_model=ClinicalDocumentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["documents"],
)
def create_document(
    payload: ClinicalDocumentCreateRequest,
    db: Session = Depends(get_db),
    service: DocumentService = Depends(get_document_service),
) -> ClinicalDocumentResponse:
    document = service.create_document(payload)
    db.commit()
    return ClinicalDocumentResponse.model_validate(document)


@router.post(
    "/documents/analyze",
    response_model=ClinicalDocumentAnalyzeResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["documents"],
)
def analyze_document(
    payload: ClinicalDocumentAnalyzeRequest,
    db: Session = Depends(get_db),
    service: DocumentService = Depends(get_document_service),
) -> ClinicalDocumentAnalyzeResponse:
    document, extraction_run = service.analyze_document(payload)
    db.commit()
    return ClinicalDocumentAnalyzeResponse(
        document=ClinicalDocumentResponse.model_validate(document),
        extraction_run=ExtractionRunResponse.model_validate(extraction_run),
    )
