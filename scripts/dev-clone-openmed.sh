#!/usr/bin/env bash
set -euo pipefail

# Clona OpenMed fuera del monorepo en ../openmed (por defecto).
# Permite sobreescribir URL y destino por variables de entorno.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OPENMED_DIR="${OPENMED_DIR:-${REPO_ROOT}/../openmed}"
OPENMED_UPSTREAM_URL="${OPENMED_UPSTREAM_URL:-https://github.com/openmed/openmed.git}"
OPENMED_FORK_URL="${OPENMED_FORK_URL:-}"

if [[ -d "${OPENMED_DIR}/.git" ]]; then
  echo "[info] Ya existe un repositorio git en: ${OPENMED_DIR}"
  echo "[info] No se realizarán cambios automáticos sobre el código de OpenMed."
  exit 0
fi

if [[ -e "${OPENMED_DIR}" && ! -d "${OPENMED_DIR}/.git" ]]; then
  echo "[error] Existe ${OPENMED_DIR}, pero no parece un repo git." >&2
  echo "[hint] Elimina ese directorio/archivo o define OPENMED_DIR a otra ruta." >&2
  exit 1
fi

echo "[info] Clonando OpenMed en: ${OPENMED_DIR}"
git clone "${OPENMED_UPSTREAM_URL}" "${OPENMED_DIR}"

if [[ -n "${OPENMED_FORK_URL}" ]]; then
  echo "[info] Configurando fork como origin: ${OPENMED_FORK_URL}"
  git -C "${OPENMED_DIR}" remote rename origin upstream
  git -C "${OPENMED_DIR}" remote add origin "${OPENMED_FORK_URL}"
  git -C "${OPENMED_DIR}" fetch origin --quiet || true
fi

echo "[ok] OpenMed disponible en ${OPENMED_DIR}"
echo "[next] Ejecuta scripts/dev-start-openmed.sh para levantar el servicio."
