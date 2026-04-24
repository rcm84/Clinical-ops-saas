"""HTTP client for OpenMed."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from .config import OpenMedConfig
from .exceptions import OpenMedHTTPStatusError, OpenMedNetworkError, OpenMedTimeoutError
from .models import HealthCheckResult, OpenMedPayload


@dataclass(frozen=True, slots=True)
class OpenMedEndpoints:
    """Endpoint path configuration.

    Defaults are intentionally conservative and can be overridden if the
    upstream API uses different routes.
    """

    health_check: str = "/health"
    analyze_text: str = "/analyze-text"
    extract_pii: str = "/extract-pii"
    deidentify_text: str = "/deidentify-text"


class OpenMedClient:
    def __init__(
        self,
        config: OpenMedConfig,
        *,
        endpoints: OpenMedEndpoints | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._config = config
        self._endpoints = endpoints or OpenMedEndpoints()
        self._http_client = http_client or httpx.Client(
            base_url=config.base_url,
            timeout=config.timeout_seconds,
        )
        self._owns_http_client = http_client is None

    def close(self) -> None:
        if self._owns_http_client:
            self._http_client.close()

    def __enter__(self) -> "OpenMedClient":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def health_check(self) -> HealthCheckResult:
        response = self._request("GET", self._endpoints.health_check)
        return HealthCheckResult(payload=self._safe_json(response), status_code=response.status_code)

    def analyze_text(self, text: str, language: str | None = None) -> OpenMedPayload:
        response = self._request(
            "POST",
            self._endpoints.analyze_text,
            json=self._text_payload(text=text, language=language),
        )
        return OpenMedPayload(payload=self._safe_json(response), status_code=response.status_code)

    def extract_pii(self, text: str, language: str | None = None) -> OpenMedPayload:
        response = self._request(
            "POST",
            self._endpoints.extract_pii,
            json=self._text_payload(text=text, language=language),
        )
        return OpenMedPayload(payload=self._safe_json(response), status_code=response.status_code)

    def deidentify_text(self, text: str, language: str | None = None) -> OpenMedPayload:
        response = self._request(
            "POST",
            self._endpoints.deidentify_text,
            json=self._text_payload(text=text, language=language),
        )
        return OpenMedPayload(payload=self._safe_json(response), status_code=response.status_code)

    def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        try:
            response = self._http_client.request(method, path, **kwargs)
        except httpx.TimeoutException as exc:
            raise OpenMedTimeoutError(
                f"Request to OpenMed timed out after {self._config.timeout_seconds} seconds."
            ) from exc
        except httpx.RequestError as exc:
            raise OpenMedNetworkError(f"Network error while calling OpenMed: {exc}") from exc

        if response.is_error:
            raise OpenMedHTTPStatusError(
                message=f"OpenMed returned HTTP {response.status_code} for {method} {path}.",
                status_code=response.status_code,
                response_text=response.text,
            )

        return response

    @staticmethod
    def _text_payload(text: str, language: str | None) -> dict[str, str]:
        payload: dict[str, str] = {"text": text}
        if language:
            payload["language"] = language
        return payload

    @staticmethod
    def _safe_json(response: httpx.Response) -> Any:
        try:
            return response.json()
        except ValueError:
            return {"raw_text": response.text}
