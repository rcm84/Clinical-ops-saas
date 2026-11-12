'use client';

import Link from 'next/link';
import { useCallback, useEffect, useState } from 'react';

import { getDocumentDetail } from '@/lib/clinicalCore';
import type { DocumentDetailResponse, ProcessingStatus } from '@/lib/types';

const POLL_INTERVAL_MS = 2000;

const ACTIVE_STATUSES: ProcessingStatus[] = ['received', 'processing'];

export default function DocumentDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const [detail, setDetail] = useState<DocumentDetailResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async (): Promise<ProcessingStatus | null> => {
    try {
      const data = await getDocumentDetail(params.id);
      setDetail(data);
      setError(null);
      return data.document.status;
    } catch (loadError) {
      setError(
        loadError instanceof Error
          ? loadError.message
          : 'Error desconocido al cargar el documento.',
      );
      return null;
    }
  }, [params.id]);

  useEffect(() => {
    let timer: ReturnType<typeof setInterval> | undefined;
    const tick = async () => {
      const status = await load();
      if ((status === 'processed' || status === 'failed' || status === null) && timer) {
        clearInterval(timer);
      }
    };
    void tick();
    timer = setInterval(() => void tick(), POLL_INTERVAL_MS);
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [load]);

  if (error) {
    return (
      <section>
        <h1>Detalle de documento</h1>
        <p className="error">Error: {error}</p>
        <p>
          <Link href="/documents/new">Crear otro documento</Link>
        </p>
      </section>
    );
  }

  if (!detail) {
    return (
      <section>
        <h1>Detalle de documento</h1>
        <p>Cargando documento {params.id}…</p>
      </section>
    );
  }

  const { document, extraction_runs } = detail;
  const isActive = ACTIVE_STATUSES.includes(document.status);

  return (
    <section>
      <h1>Detalle de documento</h1>
      <article className="card">
        <p>
          <strong>ID:</strong> {document.id}
        </p>
        <p>
          <strong>Estado:</strong> {document.status}
          {isActive ? ' (actualizando automáticamente…)' : ''}
        </p>
        <p>
          <strong>Organization ID:</strong> {document.organization_id}
        </p>
        <p>
          <strong>Patient External ID:</strong> {document.patient_external_id}
        </p>
        <p>
          <strong>Document Type:</strong> {document.document_type}
        </p>
        <p>
          <strong>Source Type:</strong> {document.source_type}
        </p>
      </article>

      <article className="card">
        <h2>Resultado de análisis</h2>
        {extraction_runs.length === 0 ? (
          <p>No existe resultado de análisis todavía.</p>
        ) : (
          extraction_runs.map((run) => (
            <div key={run.id}>
              <p>
                <strong>Run:</strong> {run.id} — {run.engine} {run.engine_version} —{' '}
                {run.status}
              </p>
              {Object.keys(run.raw_output_json).length > 0 ? (
                <pre>{JSON.stringify(run.raw_output_json, null, 2)}</pre>
              ) : (
                <p>Sin contenido por ahora.</p>
              )}
            </div>
          ))
        )}
      </article>
    </section>
  );
}
