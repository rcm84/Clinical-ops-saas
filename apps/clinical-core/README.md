# Clinical Core Service

Servicio FastAPI mínimo para operaciones clínicas con arquitectura limpia por capas.

## Estructura

```text
src/
  main.py
  api/
  domain/
  application/
  infrastructure/
  schemas/
```

## Requisitos

- Python 3.11+

## Instalación local

```bash
cd apps/clinical-core
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar el servicio

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /health` → `{"status": "ok"}`
- `POST /documents` → crea metadata básica de un documento clínico

### Ejemplo `POST /documents`

```bash
curl -X POST "http://localhost:8000/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "PAT-123",
    "title": "Evolución inicial",
    "document_type": "clinical_note",
    "created_by": "dr.garcia"
  }'
```

## Notas de arquitectura

- **api**: routers y definición de endpoints.
- **schemas**: contratos request/response con Pydantic.
- **application**: casos de uso y orquestación de lógica.
- **domain**: entidades de negocio puras.
- **infrastructure**: implementación técnica (repositorios SQLAlchemy con PostgreSQL).

## Persistencia y migraciones

- Configuración por entorno:
  - `DATABASE_URL` (default: `postgresql+psycopg://postgres:postgres@localhost:5432/clinical_core`)
  - `DB_ECHO` (`true|false`, default `false`)
- Migración inicial con Alembic en `alembic/versions/0001_initial_persistence.py`.

```bash
cd apps/clinical-core
alembic upgrade head
```

## Endpoint adicional

- `POST /documents/analyze` → persiste documento y corrida de extracción inicial.

Esta base está lista para crecer incorporando repositorios persistentes, autenticación y más casos de uso.
