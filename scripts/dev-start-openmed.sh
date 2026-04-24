#!/usr/bin/env bash
set -euo pipefail

# Inicia OpenMed desde ../openmed usando convenciones comunes.
# No modifica código en OpenMed; solo ejecuta su arranque local.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OPENMED_DIR="${OPENMED_DIR:-${REPO_ROOT}/../openmed}"
OPENMED_BASE_URL="${OPENMED_BASE_URL:-http://localhost:8080}"

if [[ ! -d "${OPENMED_DIR}" ]]; then
  echo "[error] No se encontró OpenMed en ${OPENMED_DIR}" >&2
  echo "[hint] Ejecuta scripts/dev-clone-openmed.sh primero." >&2
  exit 1
fi

if [[ -f "${OPENMED_DIR}/docker-compose.yml" || -f "${OPENMED_DIR}/compose.yaml" || -f "${OPENMED_DIR}/compose.yml" ]]; then
  echo "[info] Se detectó configuración de Docker Compose."
  (
    cd "${OPENMED_DIR}"
    docker compose up -d
  )
elif [[ -f "${OPENMED_DIR}/Makefile" ]] && grep -Eq '^run:|^dev:|^up:' "${OPENMED_DIR}/Makefile"; then
  echo "[info] Se detectó Makefile con target de desarrollo."
  (
    cd "${OPENMED_DIR}"
    if grep -q '^dev:' Makefile; then
      make dev
    elif grep -q '^run:' Makefile; then
      make run
    else
      make up
    fi
  )
else
  echo "[warn] No se detectó un método estándar de arranque automático."
  echo "[hint] Revisa el README de OpenMed y arráncalo manualmente desde: ${OPENMED_DIR}"
fi

echo "[info] Configura OPENMED_BASE_URL para Clinical SaaS: ${OPENMED_BASE_URL}"
echo "[next] Verifica conectividad ejecutando scripts/dev-check-openmed.sh"
