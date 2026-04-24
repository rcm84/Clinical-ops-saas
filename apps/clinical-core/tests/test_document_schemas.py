from __future__ import annotations

import unittest

from pydantic import ValidationError

from src.schemas.document import (
    ClinicalDocumentCreateRequest,
    ClinicalDocumentResponse,
    DocumentType,
    ProcessingStatus,
    SourceType,
)


class TestClinicalDocumentSchemas(unittest.TestCase):
    def test_create_request_valid_payload(self) -> None:
        payload = ClinicalDocumentCreateRequest.model_validate(
            {
                "organization_id": "org_123",
                "patient_external_id": "pat_987",
                "source_type": "ehr",
                "document_type": "clinical_note",
                "language": "es",
                "raw_text": "Paciente estable durante la consulta.",
            }
        )

        self.assertEqual(payload.source_type, SourceType.EHR)
        self.assertEqual(payload.document_type, DocumentType.CLINICAL_NOTE)
        self.assertEqual(payload.status, ProcessingStatus.RECEIVED)

    def test_create_request_rejects_invalid_enum(self) -> None:
        with self.assertRaises(ValidationError):
            ClinicalDocumentCreateRequest.model_validate(
                {
                    "organization_id": "org_123",
                    "patient_external_id": "pat_987",
                    "source_type": "fax",
                    "document_type": "clinical_note",
                    "language": "es",
                    "raw_text": "Texto",
                }
            )

    def test_response_requires_minimum_fields(self) -> None:
        with self.assertRaises(ValidationError):
            ClinicalDocumentResponse.model_validate(
                {
                    "id": "de0f7fbe-fd72-48f2-ad46-81b715fbb9af",
                    "organization_id": "org_123",
                }
            )


if __name__ == "__main__":
    unittest.main()
