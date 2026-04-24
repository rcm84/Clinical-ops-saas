from __future__ import annotations

from pydantic import BaseModel, Field


class DocumentJob(BaseModel):
    document_id: str = Field(..., min_length=1)
