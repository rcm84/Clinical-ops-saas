from fastapi import FastAPI

from src.api.router import router
from src.infrastructure.db.base import Base
from src.infrastructure.db import models  # noqa: F401
from src.infrastructure.db.session import engine

app = FastAPI(
    title="Clinical Core Service",
    version="0.1.0",
    description="Minimal clinical core API with clean layered architecture.",
)
app.include_router(router)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
