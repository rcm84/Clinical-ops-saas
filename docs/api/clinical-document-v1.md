# ClinicalDocument v1 (apps/clinical-core)

## Objetivo
Definir un contrato mínimo y estable para creación y lectura de documentos clínicos en `clinical-core`, manteniendo convenciones backend en `snake_case` y sin acoplamiento a ORM en esta etapa.

## Decisiones de diseño
- **Nombres en `snake_case`** para todos los campos del contrato (`organization_id`, `patient_external_id`, etc.).
- **IDs como UUID** generados en dominio (`id`) para evitar dependencia de base de datos u ORM.
- **`created_at` generado en backend** en UTC al crear la entidad.
- **Enums explícitos** para `document_type`, `source_type` y `processing_status` (campo `status`) para validar integridad del contrato desde el borde de la API.
- **Sin ORM**: persistencia temporal en repositorio en memoria (`InMemoryDocumentRepository`).

## Enums v1

### `document_type`
- `clinical_note`
- `lab_report`
- `discharge_summary`
- `prescription`
- `other`

### `source_type`
- `ehr`
- `hl7`
- `manual_upload`
- `api`

### `processing_status` (campo `status`)
- `received`
- `processing`
- `processed`
- `failed`

## Schema de entrada (create)

`ClinicalDocumentCreateRequest`

```json
{
  "organization_id": "org_123",
  "patient_external_id": "pat_987",
  "source_type": "ehr",
  "document_type": "clinical_note",
  "language": "es",
  "raw_text": "Paciente estable durante la consulta.",
  "status": "received"
}
```

Notas:
- `status` es opcional en request y por defecto toma `received`.
- `language` acepta códigos cortos (2 a 10 caracteres).

## Schema de salida

`ClinicalDocumentResponse`

```json
{
  "id": "de0f7fbe-fd72-48f2-ad46-81b715fbb9af",
  "organization_id": "org_123",
  "patient_external_id": "pat_987",
  "source_type": "ehr",
  "document_type": "clinical_note",
  "language": "es",
  "raw_text": "Paciente estable durante la consulta.",
  "status": "received",
  "created_at": "2026-04-24T12:00:00Z"
}
```

## Campos mínimos cubiertos
- `id`
- `organization_id`
- `patient_external_id`
- `source_type`
- `document_type`
- `language`
- `raw_text`
- `status`
- `created_at`
