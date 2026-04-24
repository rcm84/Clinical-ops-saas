from __future__ import annotations

from typing import List

from src.domain.entities.document import ClinicalDocument


class InMemoryDocumentRepository:
    """Temporary repository implementation while persistence is not yet defined."""

    def __init__(self) -> None:
        self._documents: List[ClinicalDocument] = []

    def save(self, document: ClinicalDocument) -> ClinicalDocument:
        self._documents.append(document)
        return document
