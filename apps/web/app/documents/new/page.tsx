'use client';

import Link from 'next/link';
import { useState } from 'react';

import { saveDocumentResult } from '@/components/document-storage';
import { analyzeDocument } from '@/lib/clinicalCore';
import type {
  AnalyzeDocumentResponse,
  DocumentType,
  SourceType,
} from '@/lib/types';

type FormState = {
  organization_id: string;
  patient_external_id: string;
  document_type: DocumentType;
  source_type: SourceType;
  language: string;
  raw_text: string;
};

const initialState: FormState = {
  organization_id: '',
  patient_external_id: '',
  document_type: 'clinical_note',
  source_type: 'manual_upload',
  language: 'es',
  raw_text: '',
};

export default function NewDocumentPage() {
  const [form, setForm] = useState<FormState>(initialState);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyzeDocumentResponse | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await analyzeDocument({
        ...form,
        extraction: {
          engine: 'openmed',
          engine_version: 'mvp',
          status: 'completed',
          raw_output_json: {},
        },
      });

      setResult(response);
      saveDocumentResult(response);
    } catch (submitError) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : 'Error desconocido al enviar documento.',
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section>
      <h1>Nuevo documento clínico</h1>

      <form onSubmit={handleSubmit} className="card form-grid">
        <label>
          Organization ID
          <input
            required
            value={form.organization_id}
            onChange={(event) =>
              setForm((prev) => ({ ...prev, organization_id: event.target.value }))
            }
          />
        </label>

        <label>
          Patient External ID
          <input
            required
            value={form.patient_external_id}
            onChange={(event) =>
              setForm((prev) => ({
                ...prev,
                patient_external_id: event.target.value,
              }))
            }
          />
        </label>

        <label>
          Document Type
          <select
            value={form.document_type}
            onChange={(event) =>
              setForm((prev) => ({
                ...prev,
                document_type: event.target.value as DocumentType,
              }))
            }
          >
            <option value="clinical_note">clinical_note</option>
            <option value="lab_report">lab_report</option>
            <option value="discharge_summary">discharge_summary</option>
            <option value="prescription">prescription</option>
            <option value="other">other</option>
          </select>
        </label>

        <label>
          Source Type
          <select
            value={form.source_type}
            onChange={(event) =>
              setForm((prev) => ({
                ...prev,
                source_type: event.target.value as SourceType,
              }))
            }
          >
            <option value="manual_upload">manual_upload</option>
            <option value="ehr">ehr</option>
            <option value="hl7">hl7</option>
            <option value="api">api</option>
          </select>
        </label>

        <label>
          Language
          <input
            required
            value={form.language}
            onChange={(event) =>
              setForm((prev) => ({ ...prev, language: event.target.value }))
            }
          />
        </label>

        <label>
          Raw Text
          <textarea
            required
            rows={8}
            value={form.raw_text}
            onChange={(event) =>
              setForm((prev) => ({ ...prev, raw_text: event.target.value }))
            }
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? 'Enviando...' : 'Enviar a clinical-core'}
        </button>
      </form>

      {error ? <p className="error">Error: {error}</p> : null}

      {result ? (
        <article className="card">
          <h2>Resultado</h2>
          <p>
            <strong>Documento ID:</strong> {result.document.id}
          </p>
          <p>
            <strong>Estado:</strong> {result.document.status}
          </p>
          <p>
            <strong>Análisis:</strong>{' '}
            {Object.keys(result.extraction_run.raw_output_json).length > 0
              ? 'Disponible'
              : 'Sin contenido por ahora'}
          </p>
          <p>
            <Link href={`/documents/${result.document.id}`}>
              Ver detalle del documento
            </Link>
          </p>
        </article>
      ) : null}
    </section>
  );
}
