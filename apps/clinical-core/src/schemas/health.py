from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Composite health: overall status plus one field per dependency."""

    status: str
    db: str = "unknown"
    redis: str = "unknown"
    openmed: str = "unknown"
