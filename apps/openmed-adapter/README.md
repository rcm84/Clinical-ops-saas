# OpenMed Adapter

Cliente Python ligero para consumir OpenMed por HTTP usando `httpx`.

## Configuración

```bash
export OPENMED_BASE_URL="https://openmed.example.com"
# opcional (default 10)
export OPENMED_TIMEOUT_SECONDS="15"
```

## Uso rápido

```python
from openmed_adapter import OpenMedClient, OpenMedConfig

config = OpenMedConfig.from_env()

with OpenMedClient(config) as client:
    health = client.health_check()
    print(health.status_code, health.payload)

    analyzed = client.analyze_text("Paciente con dolor torácico", language="es")
    print(analyzed.payload)

    pii = client.extract_pii("Nombre: Juan Pérez. Tel: 555-1234")
    print(pii.payload)

    deidentified = client.deidentify_text("Juan Pérez vive en Madrid")
    print(deidentified.payload)
```

## Manejo de errores

El cliente lanza excepciones claras:

- `OpenMedTimeoutError` para timeouts.
- `OpenMedNetworkError` para errores de red.
- `OpenMedHTTPStatusError` si la API responde con error HTTP.

Las respuestas se encapsulan en modelos Pydantic (`HealthCheckResult`, `OpenMedPayload`) y almacenan el JSON recibido en `payload` sin asumir campos no documentados.
