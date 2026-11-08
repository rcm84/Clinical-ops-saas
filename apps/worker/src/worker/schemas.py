from __future__ import annotations

from pydantic import BaseModel, Field


class DocumentJob(BaseModel):
    """Job payload in the `document_jobs` Redis queue.

    `extraction_run_id` is set by clinical-core when it enqueues the job
    (POST /documents/{id}/analyze); the worker updates that run instead of
    creating a new one. Older jobs without it still work: the worker creates
    the run itself.
    """

    document_id: str = Field(..., min_length=1)
    extraction_run_id: str | None = None
    attempts: int = Field(default=0, ge=0)
