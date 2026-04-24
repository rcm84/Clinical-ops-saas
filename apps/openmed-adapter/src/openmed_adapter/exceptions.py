"""Custom exceptions for OpenMed adapter failures."""

from __future__ import annotations


class OpenMedError(Exception):
    """Base exception for all adapter errors."""


class OpenMedNetworkError(OpenMedError):
    """Raised when a network failure occurs while calling OpenMed."""


class OpenMedTimeoutError(OpenMedNetworkError):
    """Raised when a request to OpenMed exceeds the configured timeout."""


class OpenMedHTTPStatusError(OpenMedError):
    """Raised when OpenMed returns an HTTP error response."""

    def __init__(self, message: str, status_code: int, response_text: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text
