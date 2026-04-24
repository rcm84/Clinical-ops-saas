from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, UUID, DateTime, String, Text, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from .config import settings


class Base(DeclarativeBase):
    pass


class ClinicalDocumentModel(Base):
    __tablename__ = "clinical_documents"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    language: Mapped[str] = mapped_column(String(10), nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)


class ExtractionRunModel(Base):
    __tablename__ = "extraction_runs"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    document_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    engine: Mapped[str] = mapped_column(String(100), nullable=False)
    engine_version: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    raw_output_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, class_=Session)
