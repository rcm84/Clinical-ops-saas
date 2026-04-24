from __future__ import annotations

from sqlalchemy.orm import Session

from src.domain.entities.extraction_run import ExtractionRun
from src.infrastructure.db.models import ExtractionRunModel


class SQLAlchemyExtractionRunRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, run: ExtractionRun) -> ExtractionRun:
        row = ExtractionRunModel(
            id=run.id,
            document_id=run.document_id,
            engine=run.engine,
            engine_version=run.engine_version,
            status=run.status,
            raw_output_json=run.raw_output_json,
        )
        self._session.add(row)
        self._session.flush()
        self._session.refresh(row)
        run.created_at = row.created_at
        return run
