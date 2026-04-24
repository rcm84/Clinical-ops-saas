# Worker de documentos (`apps/worker`)

Worker Python básico para procesar documentos de forma asíncrona con Redis como cola.

## Qué hace

1. Escucha trabajos en Redis (`BLPOP`) en la cola `document_jobs`.
2. Cada trabajo debe tener payload JSON con `document_id`.
3. Busca el documento en la base de datos de `clinical-core`.
4. Marca el documento como `processing`.
5. Llama a OpenMed (`POST /analyze-text`).
6. Registra un `ExtractionRun`.
7. Actualiza el documento a `processed` o `failed`.

## Payload de trabajo

```json
{"document_id": "9f5fa704-7a3f-4e8f-8ad0-4d9c8f2693e4"}
```

## Variables de entorno

- `DATABASE_URL` (default: `postgresql+psycopg://postgres:postgres@localhost:5432/clinical_core`)
- `REDIS_URL` (default: `redis://localhost:6379/0`)
- `REDIS_QUEUE_NAME` (default: `document_jobs`)
- `OPENMED_BASE_URL` (default: `http://localhost:8081`)
- `OPENMED_ANALYZE_PATH` (default: `/analyze-text`)
- `OPENMED_TIMEOUT_SECONDS` (default: `30`)

## Ejecutar local

```bash
cd apps/worker
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python -m worker.main
```

## Publicar un trabajo de ejemplo

```bash
redis-cli LPUSH document_jobs '{"document_id":"9f5fa704-7a3f-4e8f-8ad0-4d9c8f2693e4"}'
```
