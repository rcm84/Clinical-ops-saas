import type {
  AnalyzeDocumentResponse,
  ClinicalDocument,
  CreateDocumentPayload,
  DocumentDetailResponse,
} from '@/lib/types';

const CLINICAL_CORE_BASE_URL =
  process.env.NEXT_PUBLIC_CLINICAL_CORE_URL ?? 'http://localhost:4000';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${CLINICAL_CORE_BASE_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
    cache: 'no-store',
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(
      `clinical-core error (${response.status}): ${errorBody || 'unknown error'}`,
    );
  }

  return (await response.json()) as T;
}

/** POST /documents — crea el documento (estado inicial: received). */
export async function createDocument(
  payload: CreateDocumentPayload,
): Promise<ClinicalDocument> {
  return request<ClinicalDocument>('/documents', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

/** POST /documents/{id}/analyze — encola el análisis, devuelve 202. */
export async function analyzeDocument(
  documentId: string,
): Promise<AnalyzeDocumentResponse> {
  return request<AnalyzeDocumentResponse>(`/documents/${documentId}/analyze`, {
    method: 'POST',
  });
}

/** GET /documents/{id} — documento + runs, para el polling del detalle. */
export async function getDocumentDetail(
  documentId: string,
): Promise<DocumentDetailResponse> {
  return request<DocumentDetailResponse>(`/documents/${documentId}`);
}
