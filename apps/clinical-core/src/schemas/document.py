from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class DocumentCreateRequest(BaseModel):
    patient_id: str = Field(..., min_length=1, description="Patient identifier")
    title: str = Field(..., min_length=1, description="Document title")
    document_type: str = Field(..., min_length=1, description="Type/category of document")
    created_by: str = Field(..., min_length=1, description="User or system creating the document")


class DocumentResponse(BaseModel):
    id: UUID
    patient_id: str
    title: str
    document_type: str
    created_by: str
    created_at: datetime
