# Integración local con OpenMed (servicio externo)

Esta guía define un flujo mínimo para trabajar con **OpenMed como servicio externo** en el mismo workspace, sin copiar su código dentro de este monorepo.

> Convención recomendada: OpenMed vive en `../openmed` (directorio hermano de este repo).

## Principios

- OpenMed **no** forma parte de este monorepo.
- Este repo se integra con OpenMed únicamente vía red usando `OPENMED_BASE_URL`.
- No se debe copiar código de OpenMed aquí.
- No se modifica OpenMed desde scripts de este repositorio.

## 1) Clonar OpenMed fuera del monorepo

### Opción A: clonar upstream (lo habitual al empezar)

Úsala cuando solo necesitas ejecutar OpenMed localmente y no planeas subir cambios a corto plazo.

```bash
scripts/dev-clone-openmed.sh
```

Por defecto clona en `../openmed` desde:

- `https://github.com/openmed/openmed.git` (upstream por defecto del script).

También puedes sobreescribir rutas/URLs:

```bash
OPENMED_DIR="../openmed" \
OPENMED_UPSTREAM_URL="https://github.com/openmed/openmed.git" \
scripts/dev-clone-openmed.sh
```

### Opción B: usar fork propio (cuando sí harás cambios)

Conviene usar fork cuando:

- vas a modificar OpenMed;
- necesitas ramas propias de larga vida;
- quieres abrir PRs hacia upstream desde tu fork.

Ejemplo configurando fork desde el inicio:

```bash
OPENMED_FORK_URL="git@github.com:tu-org/openmed.git" \
scripts/dev-clone-openmed.sh
```

Con eso, el script deja:

- `upstream` apuntando al repo oficial;
- `origin` apuntando a tu fork.

## 2) Levantar OpenMed localmente

```bash
scripts/dev-start-openmed.sh
```

El script intenta mecanismos comunes:

1. `docker compose up -d` si detecta archivos Compose.
2. `make dev` / `make run` / `make up` si detecta `Makefile` con esos targets.
3. Si no detecta nada estándar, imprime instrucciones para arranque manual.

> Si OpenMed requiere pasos extra (variables, seeds, migraciones), ejecútalos dentro de `../openmed` según su documentación.

## 3) Configurar el SaaS para consumir OpenMed

El contrato de integración es:

```bash
export OPENMED_BASE_URL="http://localhost:8080"
```

Si ejecutas `clinical-core` localmente, exporta esa variable en la misma sesión antes de iniciar el servicio.

## 4) Health checks y verificación de conectividad

### Health check directo a OpenMed

Comandos manuales útiles:

```bash
curl -i "$OPENMED_BASE_URL/health"
curl -i "$OPENMED_BASE_URL/healthz"
```

### Verificación automática (incluye prueba desde clinical-core)

```bash
scripts/dev-check-openmed.sh
```

Este script:

- prueba endpoints de salud en OpenMed (`/health`, `/healthz`, `/live`, `/`);
- y luego ejecuta una verificación HTTP desde el contexto de `apps/clinical-core` para confirmar que el servicio del SaaS puede alcanzar `OPENMED_BASE_URL`.

## 5) Migrar de upstream a fork más adelante

Si empezaste con clone simple y luego necesitas cambios:

1. crea un fork en GitHub;
2. en `../openmed`, agrega/configura remotos:

```bash
cd ../openmed
git remote rename origin upstream
git remote add origin git@github.com:tu-org/openmed.git
git fetch --all
```

3. trabaja en ramas de tu fork y abre PRs hacia upstream cuando corresponda.

Así mantienes este monorepo desacoplado y sigues integrando por `OPENMED_BASE_URL`.
