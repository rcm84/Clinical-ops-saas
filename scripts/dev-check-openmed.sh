#!/usr/bin/env bash
set -euo pipefail

# Verificación mínima de conectividad hacia OpenMed y prueba desde clinical-core.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OPENMED_BASE_URL="${OPENMED_BASE_URL:-http://localhost:8080}"

HEALTH_PATHS=("/health" "/healthz" "/live" "/")

echo "[info] OPENMED_BASE_URL=${OPENMED_BASE_URL}"
echo "[info] Intentando health checks HTTP..."

check_ok=0
for path in "${HEALTH_PATHS[@]}"; do
  url="${OPENMED_BASE_URL%/}${path}"
  status="$(curl -sS -o /tmp/openmed-health.out -w '%{http_code}' "${url}" || true)"
  if [[ "${status}" =~ ^2|3 ]]; then
    echo "[ok] ${url} -> HTTP ${status}"
    check_ok=1
    break
  fi
  echo "[info] ${url} -> HTTP ${status}"
done

if [[ "${check_ok}" -ne 1 ]]; then
  echo "[error] No fue posible validar health check de OpenMed." >&2
  exit 1
fi

echo "[info] Verificando desde contexto de clinical-core (urllib estándar)..."
(
  cd "${REPO_ROOT}/apps/clinical-core"
  OPENMED_BASE_URL="${OPENMED_BASE_URL}" python - <<'PY'
import json
import os
import urllib.request

base = os.environ["OPENMED_BASE_URL"].rstrip("/")
url = f"{base}/health"

try:
    with urllib.request.urlopen(url, timeout=5) as resp:
        body = resp.read(300).decode("utf-8", errors="replace")
        print(f"[ok] clinical-core -> {url} | status={resp.status}")
        print(f"[body] {body}")
except Exception as exc:
    raise SystemExit(f"[error] clinical-core no pudo conectar a {url}: {exc}")
PY
)

echo "[ok] Conectividad OpenMed validada para uso con OPENMED_BASE_URL."
