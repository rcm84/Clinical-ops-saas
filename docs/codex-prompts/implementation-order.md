# Orden de implementación (rápido, sin sobrearquitectura)

> Objetivo: pasar de “repo base” a un MVP usable en el menor tiempo posible, priorizando flujo end-to-end y validación temprana con usuarios.

## Principios de ejecución

- **Vertical slices primero**: implementar flujos completos (UI → API → worker → persistencia) antes que capas “perfectas”.
- **Una fuente de verdad mínima**: `clinical-core` concentra estado de documentos y ejecuciones.
- **Acoplamiento pragmático**: integración directa entre servicios vía HTTP/cola; evitar abstracciones prematuras.
- **Done > perfecto**: si algo no desbloquea al usuario del MVP, se posterga.

---

## Orden recomendado de implementación (fases)

## Fase 0 — Bootstrap funcional (día 0-1)

**Objetivo:** todo levanta local y hay smoke flow básico.

1. Configurar entorno local (`docker-compose`, variables `.env`).
2. Verificar health checks de `clinical-core`, `worker`, `openmed-adapter`, `web`.
3. Crear script/checklist de arranque único para el equipo.

**Valor:** elimina fricción del equipo y reduce tiempo muerto antes de codificar features.

## Fase 1 — Ingesta y persistencia mínima (día 1-3)

**Objetivo:** crear documento y guardarlo con estado trazable.

1. Endpoint en `clinical-core` para crear/listar/obtener documentos.
2. Persistencia base en DB (modelo `Document` + migración mínima).
3. UI en `web` para alta/listado simple.

**Valor:** primer loop visible para usuario interno.

## Fase 2 — Orquestación de extracción (día 3-5)

**Objetivo:** disparar procesamiento asíncrono y reflejar estado.

1. Encolar job desde `clinical-core` al crear documento (o acción explícita de “procesar”).
2. `worker` consume job y llama `openmed-adapter`.
3. Guardar resultado/resumen de extracción y estado final (`pending` → `processing` → `done`/`failed`).

**Valor:** primer flujo end-to-end real del producto.

## Fase 3 — Visualización clínica usable (día 5-7)

**Objetivo:** mostrar resultado en UI con foco de decisión.

1. Pantalla de detalle de documento con estado y datos extraídos.
2. Manejo básico de errores/reintento manual.
3. Indicadores mínimos de confianza/calidad (si existen en respuesta).

**Valor:** habilita validación funcional con stakeholders clínicos.

## Fase 4 — Hardening MVP (día 7-10)

**Objetivo:** dejar MVP operable para piloto interno.

1. Logging estructurado y correlación por `document_id` / `run_id`.
2. Timeouts/retries acotados en integraciones externas.
3. Métricas mínimas (jobs procesados, tasa de error, latencia).
4. Documentación operativa breve (runbook de fallas comunes).

**Valor:** reduce riesgo operativo sin caer en plataforma enterprise.

---

## Qué prompts correr primero (secuencia sugerida)

> Diseñado para usar Codex de forma incremental. Ejecutar cada prompt sólo cuando el anterior esté en verde.

1. **Prompt de mapeo rápido**
   - “Mapea arquitectura actual por servicio (`web`, `clinical-core`, `worker`, `openmed-adapter`) y enumera gaps para flujo MVP de documento→extracción→visualización.”
2. **Prompt de slice 1 (CRUD documento)**
   - “Implementa alta/listado/detalle de documentos de punta a punta (web + API + DB) con tests mínimos.”
3. **Prompt de slice 2 (job async)**
   - “Agrega disparo de procesamiento asíncrono desde `clinical-core` y consumo en `worker` con transición de estados.”
4. **Prompt de slice 3 (integración OpenMed)**
   - “Conecta `worker` con `openmed-adapter`, persiste resultado resumido y maneja errores transitorios con retry acotado.”
5. **Prompt de slice 4 (UI clínica)**
   - “Construye vista de detalle con estado de procesamiento, resultado extraído y acción de reintento.”
6. **Prompt de hardening MVP**
   - “Añade logging estructurado, métricas básicas y checklist de operación para piloto.”

Regla práctica: **evitar prompts de refactor general** antes de tener 1 flujo completo en producción interna.

---

## Dependencias entre servicios (mínimas y reales)

- `web` depende de `clinical-core` para CRUD y consulta de estados/resultados.
- `clinical-core` depende de DB para persistencia de documentos y runs.
- `clinical-core` depende de cola (o mecanismo async elegido) para publicar trabajos.
- `worker` depende de cola para consumir trabajos.
- `worker` depende de `openmed-adapter` para extracción clínica.
- `worker` depende de `clinical-core`/DB (según diseño actual) para persistir estado final.

### Cadena crítica del MVP

`web` → `clinical-core` → `queue` → `worker` → `openmed-adapter` → `clinical-core/DB` → `web`

Si esta cadena no funciona de extremo a extremo, **nada más importa** para MVP.

---

## Checklist de MVP (rápida)

- [ ] Crear documento desde UI.
- [ ] Ver documento en listado y detalle.
- [ ] Disparar procesamiento (automático o manual).
- [ ] Ver transición de estado en UI (`pending/processing/done/failed`).
- [ ] Persistir resultado de extracción.
- [ ] Mostrar resultado resumido en detalle.
- [ ] Reintentar procesamiento fallido.
- [ ] Logs con trazabilidad por documento.
- [ ] README/runbook con pasos de arranque + troubleshooting básico.

---

## Criterios de “done” por fase

## Fase 0 done

- Todos los servicios levantan localmente con un solo comando.
- Existe verificación simple de salud por servicio.
- Cualquier dev nuevo puede levantar entorno en < 30 min.

## Fase 1 done

- CRUD mínimo de documentos operativo desde UI.
- Datos persisten en DB tras reinicio de servicios.
- Tests básicos de esquema/API en verde.

## Fase 2 done

- Un documento puede pasar por ciclo async completo.
- Estados de procesamiento se reflejan correctamente.
- Fallas transitorias no rompen el sistema (al menos 1 retry controlado).

## Fase 3 done

- Usuario puede interpretar resultado sin mirar logs.
- Errores visibles con acción de reintento.
- Tiempo de feedback aceptable para operación (objetivo práctico del equipo).

## Fase 4 done

- Logs y métricas permiten diagnosticar incidentes comunes.
- Existe runbook corto para recuperar fallas típicas.
- Se puede operar piloto interno con intervención manual limitada.

---

## Anti-sobrearquitectura (guardrails)

- No introducir event bus complejo si una cola simple ya cubre el flujo.
- No separar microservicios adicionales durante MVP.
- No diseñar “framework interno” de extracción antes de validar 1 proveedor.
- No bloquear entrega por cobertura de test exhaustiva: priorizar tests de camino crítico.
- No optimizar rendimiento antes de tener métricas reales de cuello de botella.

En resumen: **primero flujo end-to-end, luego robustez puntual, después escalado.**
