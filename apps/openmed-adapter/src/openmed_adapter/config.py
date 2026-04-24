"""Runtime configuration for the OpenMed adapter."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OpenMedConfig:
    """Configuration required to talk to OpenMed over HTTP."""

    base_url: str
    timeout_seconds: float = 10.0

    @classmethod
    def from_env(cls) -> "OpenMedConfig":
        base_url = os.getenv("OPENMED_BASE_URL")
        if not base_url:
            raise ValueError(
                "OPENMED_BASE_URL is not set. Define OPENMED_BASE_URL with the OpenMed API URL."
            )
        timeout_raw = os.getenv("OPENMED_TIMEOUT_SECONDS")
        timeout_seconds = float(timeout_raw) if timeout_raw else 10.0
        return cls(base_url=base_url, timeout_seconds=timeout_seconds)
