from __future__ import annotations

import os


class DatabaseSettings:
    def __init__(self) -> None:
        self.url = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://postgres:postgres@localhost:5432/clinical_core",
        )
        self.echo = os.getenv("DB_ECHO", "false").lower() == "true"


settings = DatabaseSettings()
