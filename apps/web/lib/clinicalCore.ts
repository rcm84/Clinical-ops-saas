import type { AnalyzeDocumentPayload, AnalyzeDocumentResponse } from '@/lib/types';

const CLINICAL_CORE_BASE_URL =
  process.env.NEXT_PUBLIC_CLINICAL_CORE_URL ?? 'http://localhost:8000';

export async function analyzeDocument(
  payload: AnalyzeDocumentPayload,
): Promise<AnalyzeDocumentResponse> {
  const response = await fetch(`${CLINICAL_CORE_BASE_URL}/documents/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
    cache: 'no-store',
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(
      `clinical-core error (${response.status}): ${errorBody || 'unknown error'}`,
    );
  }

  return (await response.json()) as AnalyzeDocumentResponse;
}
