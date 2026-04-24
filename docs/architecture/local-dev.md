# Local development con Docker Compose

Este documento describe un entorno local **mínimo** para el monorepo usando `docker-compose.yml`.

## Servicios incluidos

- `postgres`: base de datos PostgreSQL con volumen persistente.
- `redis`: caché/cola simple para desarrollo.
- `openmed`: servicio separado para capacidades clínicas (preparado para `build` desde un Dockerfile externo).
- `clinical-core`: placeholder del backend principal.
- `web`: placeholder del frontend.

## Requisitos previos

- Docker Engine + Docker Compose v2.

## Arranque del entorno

Desde la raíz del repositorio:

```bash
docker compose up -d
```

Para ver logs:

```bash
docker compose logs -f
```

Para apagar y remover contenedores:

```bash
docker compose down
```

## Configuración de OpenMed

En este monorepo no se asume una imagen pública de OpenMed. Por eso el servicio `openmed` está definido con `build`:

- `context: ../openmed`
- `dockerfile: Dockerfile`

Si tu código de OpenMed está en otra ubicación, ajusta esas rutas. Si ya tienes una imagen válida, reemplaza `build:` por algo como:

```yaml
image: ghcr.io/tu-org/openmed:dev
```

## Variables y conectividad entre servicios

`clinical-core` recibe:

- `DATABASE_URL=postgresql://clinical_user:clinical_pass@postgres:5432/clinical_ops`
- `REDIS_URL=redis://redis:6379`
- `OPENMED_BASE_URL=http://openmed:8080`

Clave importante: dentro de Docker Compose se usa el nombre de servicio (`openmed`) como hostname DNS interno.

## Puertos expuestos (host -> contenedor)

- PostgreSQL: `5432 -> 5432`
- Redis: `6379 -> 6379`
- OpenMed: `8080 -> 8080`
- clinical-core (placeholder): `4000 -> 4000`
- web (placeholder): `3000 -> 3000`

## Persistencia de datos

- `postgres-data`: datos de PostgreSQL.
- `redis-data`: persistencia AOF de Redis en desarrollo.

## Notas sobre placeholders

- `clinical-core` y `web` usan temporalmente `busybox` con un proceso en espera (`sleep infinity`) para mantener la topología y variables de entorno.
- Cuando existan Dockerfiles reales, sustituye cada placeholder por `build:` o `image:` definitivos.
