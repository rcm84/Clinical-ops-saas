'use client';

import { useMemo } from 'react';

import { getDocumentResultById } from '@/components/document-storage';

export default function DocumentDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const result = useMemo(() => getDocumentResultById(params.id), [params.id]);

  if (!result) {
    return (
      <section>
        <h1>Detalle de documento</h1>
        <p>
          No hay datos guardados localmente para el documento <code>{params.id}</code>.
        </p>
        <p>
          Crea un documento desde <code>/documents/new</code> para ver su detalle.
        </p>
      </section>
    );
  }

  return (
    <section>
      <h1>Detalle de documento</h1>
      <article className="card">
        <p>
          <strong>ID:</strong> {result.document.id}
        </p>
        <p>
          <strong>Estado:</strong> {result.document.status}
        </p>
        <p>
          <strong>Organization ID:</strong> {result.document.organization_id}
        </p>
        <p>
          <strong>Patient External ID:</strong> {result.document.patient_external_id}
        </p>
        <p>
          <strong>Document Type:</strong> {result.document.document_type}
        </p>
        <p>
          <strong>Source Type:</strong> {result.document.source_type}
        </p>
      </article>

      <article className="card">
        <h2>Resultado de análisis</h2>
        {Object.keys(result.extraction_run.raw_output_json).length > 0 ? (
          <pre>{JSON.stringify(result.extraction_run.raw_output_json, null, 2)}</pre>
        ) : (
          <p>No existe resultado de análisis todavía.</p>
        )}
      </article>
    </section>
  );
}
