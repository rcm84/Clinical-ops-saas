export type DocumentType =
  | 'clinical_note'
  | 'lab_report'
  | 'discharge_summary'
  | 'prescription'
  | 'other';

export type SourceType = 'ehr' | 'hl7' | 'manual_upload' | 'api';

export type ProcessingStatus = 'received' | 'processing' | 'processed' | 'failed';

export type CreateDocumentPayload = {
  organization_id: string;
  patient_external_id: string;
  document_type: DocumentType;
  source_type: SourceType;
  language: string;
  raw_text: string;
  status?: ProcessingStatus;
};

export type ClinicalDocument = {
  id: string;
  organization_id: string;
  patient_external_id: string;
  source_type: SourceType;
  document_type: DocumentType;
  language: string;
  raw_text: string;
  status: ProcessingStatus;
  created_at: string;
};

export type ExtractionRun = {
  id: string;
  document_id: string;
  engine: string;
  engine_version: string;
  status: string;
  raw_output_json: Record<string, unknown>;
  created_at: string;
};

export type DocumentDetailResponse = {
  document: ClinicalDocument;
  extraction_runs: ExtractionRun[];
};

export type AnalyzeDocumentResponse = {
  document: ClinicalDocument;
  extraction_run: ExtractionRun;
};
