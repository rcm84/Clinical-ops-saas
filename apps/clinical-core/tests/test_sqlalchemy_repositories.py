from __future__ import annotations

import unittest

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from src.domain.entities.document import ClinicalDocument
from src.domain.entities.extraction_run import ExtractionRun
from src.infrastructure.db.base import Base
from src.infrastructure.db.models import ClinicalDocumentModel, ExtractionRunModel
from src.infrastructure.repositories.sqlalchemy_document_repository import SQLAlchemyDocumentRepository
from src.infrastructure.repositories.sqlalchemy_extraction_run_repository import SQLAlchemyExtractionRunRepository
from src.schemas.document import DocumentType, ProcessingStatus, SourceType


class TestSQLAlchemyRepositories(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine, class_=Session)

    def test_document_repository_persists_document(self) -> None:
        with self.session_factory() as session:
            repository = SQLAlchemyDocumentRepository(session=session)
            doc = ClinicalDocument(
                organization_id="org_1",
                patient_external_id="pat_1",
                source_type=SourceType.EHR,
                document_type=DocumentType.CLINICAL_NOTE,
                language="es",
                raw_text="Paciente estable",
                status=ProcessingStatus.RECEIVED,
            )

            saved = repository.save(doc)
            session.commit()

            row = session.execute(select(ClinicalDocumentModel).where(ClinicalDocumentModel.id == saved.id)).scalar_one()
            self.assertEqual(row.organization_id, "org_1")
            self.assertEqual(row.status, "received")

    def test_extraction_run_repository_persists_run(self) -> None:
        with self.session_factory() as session:
            doc_repo = SQLAlchemyDocumentRepository(session=session)
            run_repo = SQLAlchemyExtractionRunRepository(session=session)

            doc = doc_repo.save(
                ClinicalDocument(
                    organization_id="org_1",
                    patient_external_id="pat_1",
                    source_type=SourceType.EHR,
                    document_type=DocumentType.CLINICAL_NOTE,
                    language="es",
                    raw_text="Paciente estable",
                )
            )
            run = ExtractionRun(
                document_id=doc.id,
                engine="mock-llm",
                engine_version="v1",
                status="completed",
                raw_output_json={"entities": []},
            )

            saved_run = run_repo.save(run)
            session.commit()

            row = session.execute(select(ExtractionRunModel).where(ExtractionRunModel.id == saved_run.id)).scalar_one()
            self.assertEqual(str(row.document_id), str(doc.id))
            self.assertEqual(row.engine, "mock-llm")


if __name__ == "__main__":
    unittest.main()
