# clinical-ops-saas

Monorepo inicial para un SaaS orientado a transformar documentos clínicos en datos estructurados.

La plataforma usará **OpenMed** como servicio externo para extracción y normalización clínica, y expondrá capacidades internas mediante servicios desacoplados.

## Estructura del repositorio

- `apps/`: aplicaciones y servicios principales del producto.
  - `web/`: frontend de la plataforma (portal de usuarios y operaciones).
  - `gateway/`: API gateway/BFF para autenticación, agregación y enrutamiento.
  - `clinical-core/`: lógica principal de negocio clínico y orquestación.
  - `openmed-adapter/`: integración con OpenMed (cliente, mapeos y transformación).
  - `worker/`: procesamiento asíncrono (colas, jobs, tareas batch).
- `packages/`: paquetes compartidos entre apps.
  - `shared-types/`: tipos y contratos comunes.
  - `shared-config/`: configuración reutilizable por entorno/servicio.
  - `sdk-ts/`: SDK TypeScript para consumir capacidades del sistema.
- `infra/`: infraestructura y automatización.
  - `docker/`: recursos de contenedorización.
  - `terraform/`: infraestructura como código.
  - `github-actions/`: plantillas/workflows de CI/CD.
- `docs/`: documentación técnica y funcional.
  - `architecture/`: decisiones y diagramas de arquitectura.
  - `api/`: especificaciones y guías de API.
  - `codex-prompts/`: prompts y guías operativas para agentes.
- `scripts/`: scripts auxiliares de desarrollo y automatización.

## Estado actual

Este repositorio contiene únicamente la estructura base inicial. Aún no se incluye lógica de negocio ni implementación de servicios.
