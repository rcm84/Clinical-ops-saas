import type { AnalyzeDocumentResponse } from '@/lib/types';

const STORAGE_KEY = 'clinical-documents-mvp';

function canUseStorage(): boolean {
  return typeof window !== 'undefined' && typeof localStorage !== 'undefined';
}

export function saveDocumentResult(result: AnalyzeDocumentResponse): void {
  if (!canUseStorage()) {
    return;
  }

  const current = getDocumentResultsMap();
  current[result.document.id] = result;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(current));
}

export function getDocumentResultById(
  id: string,
): AnalyzeDocumentResponse | null {
  if (!canUseStorage()) {
    return null;
  }

  const current = getDocumentResultsMap();
  return current[id] ?? null;
}

function getDocumentResultsMap(): Record<string, AnalyzeDocumentResponse> {
  if (!canUseStorage()) {
    return {};
  }

  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return {};
  }

  try {
    return JSON.parse(raw) as Record<string, AnalyzeDocumentResponse>;
  } catch {
    return {};
  }
}
