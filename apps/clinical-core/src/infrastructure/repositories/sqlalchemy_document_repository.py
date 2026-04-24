from __future__ import annotations

from sqlalchemy.orm import Session

from src.domain.entities.document import ClinicalDocument
from src.infrastructure.db.models import ClinicalDocumentModel


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
