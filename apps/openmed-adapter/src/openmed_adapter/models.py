"""Typed payload wrappers returned by OpenMed adapter methods."""

from __future__ import annotations

from typing import Any, Dict, List, Union

from pydantic import BaseModel, ConfigDict

JSONValue = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]


class OpenMedPayload(BaseModel):
    """Safe wrapper around non-documented OpenMed JSON responses."""

    model_config = ConfigDict(extra="ignore")

    payload: JSONValue
    status_code: int


class HealthCheckResult(OpenMedPayload):
    """Typed model returned by health_check."""
