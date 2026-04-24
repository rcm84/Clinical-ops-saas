from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.schemas.document import DocumentType, ProcessingStatus, SourceType


@dataclass(slots=True)
class ClinicalDocument:
    """Core domain entity for a clinical document."""

    organization_id: str
    patient_external_id: str
    source_type: SourceType
    document_type: DocumentType
    language: str
    raw_text: str
    status: ProcessingStatus = ProcessingStatus.RECEIVED
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
