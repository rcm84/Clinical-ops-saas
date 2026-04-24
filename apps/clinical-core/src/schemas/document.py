from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DocumentType(str, Enum):
    CLINICAL_NOTE = "clinical_note"
    LAB_REPORT = "lab_report"
    DISCHARGE_SUMMARY = "discharge_summary"
    PRESCRIPTION = "prescription"
    OTHER = "other"


class SourceType(str, Enum):
    EHR = "ehr"
    HL7 = "hl7"
    MANUAL_UPLOAD = "manual_upload"
    API = "api"


class ProcessingStatus(str, Enum):
    RECEIVED = "received"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class ClinicalDocumentCreateRequest(BaseModel):
    organization_id: str = Field(..., min_length=1, description="Organization identifier")
    patient_external_id: str = Field(..., min_length=1, description="External patient identifier")
    source_type: SourceType
    document_type: DocumentType
    language: str = Field(..., min_length=2, max_length=10, description="Document language code")
    raw_text: str = Field(..., min_length=1, description="Raw source text")
    status: ProcessingStatus = Field(default=ProcessingStatus.RECEIVED)


class ClinicalDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: str
    patient_external_id: str
    source_type: SourceType
    document_type: DocumentType
    language: str
    raw_text: str
    status: ProcessingStatus
    created_at: datetime


class ExtractionRunCreateRequest(BaseModel):
    engine: str = Field(..., min_length=1)
    engine_version: str = Field(..., min_length=1)
    status: str = Field(default="completed", min_length=1)
    raw_output_json: dict[str, Any] = Field(default_factory=dict)


class ClinicalDocumentAnalyzeRequest(ClinicalDocumentCreateRequest):
    extraction: ExtractionRunCreateRequest


class ExtractionRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    document_id: UUID
    engine: str
    engine_version: str
    status: str
    raw_output_json: dict[str, Any]
    created_at: datetime


class ClinicalDocumentAnalyzeResponse(BaseModel):
    document: ClinicalDocumentResponse
    extraction_run: ExtractionRunResponse
