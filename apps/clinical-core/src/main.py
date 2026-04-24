from fastapi import FastAPI

from src.api.router import router

app = FastAPI(
    title="Clinical Core Service",
    version="0.1.0",
    description="Minimal clinical core API with clean layered architecture.",
)
app.include_router(router)
