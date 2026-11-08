from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
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

    def get_by_id(self, run_id: UUID) -> ExtractionRun | None:
        row = self._session.get(ExtractionRunModel, run_id)
        if row is None:
            return None
        return self._to_entity(row)

    def get_by_document_id(self, document_id: UUID) -> list[ExtractionRun]:
        rows = self._session.execute(
            select(ExtractionRunModel)
            .where(ExtractionRunModel.document_id == document_id)
            .order_by(ExtractionRunModel.created_at)
        ).scalars().all()
        return [self._to_entity(row) for row in rows]

    @staticmethod
    def _to_entity(row: ExtractionRunModel) -> ExtractionRun:
        return ExtractionRun(
            document_id=row.document_id,
            engine=row.engine,
            engine_version=row.engine_version,
            status=row.status,
            raw_output_json=row.raw_output_json,
            id=row.id,
            created_at=row.created_at,
        )
