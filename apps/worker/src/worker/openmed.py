from __future__ import annotations

from typing import Any

import httpx

from .config import settings


class OpenMedClient:
    def __init__(self) -> None:
        self._http_client = httpx.Client(
            base_url=settings.openmed_base_url,
            timeout=settings.openmed_timeout_seconds,
        )

    def close(self) -> None:
        self._http_client.close()

    def analyze_text(self, text: str, language: str) -> dict[str, Any]:
        response = self._http_client.post(
            settings.openmed_analyze_path,
            json={"text": text, "language": language},
        )
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return {"raw_text": response.text}
