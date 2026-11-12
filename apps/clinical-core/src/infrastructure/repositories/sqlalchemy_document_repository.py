from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.entities.document import ClinicalDocument
from src.infrastructure.db.models import ClinicalDocumentModel
from src.schemas.document import DocumentType, ProcessingStatus, SourceType


class SQLAlchemyDocumentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, document: ClinicalDocument) -> ClinicalDocument:
        row = ClinicalDocumentModel(
            id=document.id,
            organization_id=document.organization_id,
            patient_external_id=document.patient_external_id,
            source_type=document.source_type.value,
            document_type=document.document_type.value,
            language=document.language,
            raw_text=document.raw_text,
            status=document.status.value,
        )
        self._session.add(row)
        self._session.flush()
        self._session.refresh(row)
        document.created_at = row.created_at
        return document

    def get_by_id(self, document_id: UUID) -> ClinicalDocument | None:
        row = self._session.get(ClinicalDocumentModel, document_id)
        if row is None:
            return None
        return ClinicalDocument(
            organization_id=row.organization_id,
            patient_external_id=row.patient_external_id,
            source_type=SourceType(row.source_type),
            document_type=DocumentType(row.document_type),
            language=row.language,
            raw_text=row.raw_text,
            status=ProcessingStatus(row.status),
            id=row.id,
            created_at=row.created_at,
        )

    def update_status(self, document_id: UUID, status: ProcessingStatus) -> None:
        row = self._session.get(ClinicalDocumentModel, document_id)
        if row is None:
            return
        row.status = status.value
        self._session.flush()
