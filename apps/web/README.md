# Web MVP (Next.js)

App mínima en Next.js (TypeScript) para flujo interno de documentos clínicos.

## Rutas

- `/` landing interna
- `/documents/new` formulario de carga y envío
- `/documents/[id]` detalle básico con datos guardados localmente

## Configuración

Variable opcional:

- `NEXT_PUBLIC_CLINICAL_CORE_URL` (default: `http://localhost:8000`)

## Desarrollo

```bash
cd apps/web
npm install
npm run dev
```
