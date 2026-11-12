from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.router import router
from src.infrastructure.db.base import Base
from src.infrastructure.db import models  # noqa: F401
from src.infrastructure.db.session import engine
from src.infrastructure.settings import settings

app = FastAPI(
    title="Clinical Core Service",
    version="0.1.0",
    description="Minimal clinical core API with clean layered architecture.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
