from __future__ import annotations

from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.application.services.document_service import DocumentService
from src.infrastructure.db.session import get_db
from src.infrastructure.queue.redis_queue import RedisQueue
from src.infrastructure.repositories.sqlalchemy_document_repository import SQLAlchemyDocumentRepository
from src.infrastructure.repositories.sqlalchemy_extraction_run_repository import SQLAlchemyExtractionRunRepository
from src.infrastructure.settings import settings
from src.schemas.document import (
    ClinicalDocumentAnalyzeRequest,
    ClinicalDocumentAnalyzeResponse,
    ClinicalDocumentCreateRequest,
    ClinicalDocumentResponse,
    DocumentDetailResponse,
    ExtractionRunResponse,
)
from src.schemas.health import HealthResponse

router = APIRouter()


def get_document_service(db: Session = Depends(get_db)) -> DocumentService:
    return DocumentService(
        document_repository=SQLAlchemyDocumentRepository(session=db),
        extraction_run_repository=SQLAlchemyExtractionRunRepository(session=db),
    )


def get_redis_queue() -> RedisQueue:
    return RedisQueue()


def _check_db(db: Session) -> str:
    try:
        db.execute(text("SELECT 1"))
        return "ok"
    except Exception:
        return "error"


def _check_redis(queue: RedisQueue) -> str:
    return "ok" if queue.ping() else "error"


def _check_openmed() -> str:
    try:
        with httpx.Client(base_url=settings.openmed_base_url, timeout=2.0) as client:
            response = client.get("/health")
        return "ok" if response.status_code < 400 else "error"
    except httpx.HTTPError:
        return "error"


@router.get("/health", response_model=HealthResponse, tags=["health"])
def health_check(
    db: Session = Depends(get_db),
    queue: RedisQueue = Depends(get_redis_queue),
) -> HealthResponse:
    """Composite health: DB + Redis + OpenMed.

    Always returns HTTP 200 so the container healthcheck only fails when the
    API itself is down; the `status` field is "ok" or "degraded".
    """
    checks = {
        "db": _check_db(db),
        "redis": _check_redis(queue),
        "openmed": _check_openmed(),
    }
    overall = "ok" if all(value == "ok" for value in checks.values()) else "degraded"
    return HealthResponse(status=overall, **checks)


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


@router.get(
    "/documents/{document_id}",
    response_model=DocumentDetailResponse,
    tags=["documents"],
)
def get_document_detail(
    document_id: UUID,
    service: DocumentService = Depends(get_document_service),
) -> DocumentDetailResponse:
    document = service.get_document(document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    runs = service.list_extraction_runs(document_id)
    return DocumentDetailResponse(
        document=ClinicalDocumentResponse.model_validate(document),
        extraction_runs=[ExtractionRunResponse.model_validate(run) for run in runs],
    )


@router.post(
    "/documents/{document_id}/analyze",
    response_model=ClinicalDocumentAnalyzeResponse,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["documents"],
)
def analyze_document_async(
    document_id: UUID,
    db: Session = Depends(get_db),
    service: DocumentService = Depends(get_document_service),
    queue: RedisQueue = Depends(get_redis_queue),
) -> ClinicalDocumentAnalyzeResponse:
    """Enqueue an OpenMed analysis job and return 202.

    Creates an extraction run in status "queued", marks the document as
    "processing" and pushes {document_id, extraction_run_id} to the
    `document_jobs` Redis queue for the worker.
    """
    prepared = service.prepare_analysis(document_id)
    if prepared is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    document, extraction_run = prepared
    db.commit()
    try:
        queue.push_analysis_job(document_id=document.id, extraction_run_id=extraction_run.id)
    except Exception as exc:
        # The run stays "queued" in DB; the client can retry the analyze call.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not enqueue analysis job: {exc}",
        ) from exc
    return ClinicalDocumentAnalyzeResponse(
        document=ClinicalDocumentResponse.model_validate(document),
        extraction_run=ExtractionRunResponse.model_validate(extraction_run),
    )


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
    """Legacy synchronous analyze (caller provides the extraction output).

    Kept for compatibility; new clients use POST /documents/{id}/analyze.
    """
    document, extraction_run = service.analyze_document(payload)
    db.commit()
    return ClinicalDocumentAnalyzeResponse(
        document=ClinicalDocumentResponse.model_validate(document),
        extraction_run=ExtractionRunResponse.model_validate(extraction_run),
    )
