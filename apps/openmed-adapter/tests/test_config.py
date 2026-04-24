import pytest

from openmed_adapter import OpenMedConfig


def test_from_env_reads_base_url(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("OPENMED_BASE_URL", "https://openmed.test")
    monkeypatch.setenv("OPENMED_TIMEOUT_SECONDS", "7.5")

    config = OpenMedConfig.from_env()

    assert config.base_url == "https://openmed.test"
    assert config.timeout_seconds == 7.5


def test_from_env_requires_base_url(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("OPENMED_BASE_URL", raising=False)
    monkeypatch.delenv("OPENMED_TIMEOUT_SECONDS", raising=False)

    with pytest.raises(ValueError, match="OPENMED_BASE_URL"):
        OpenMedConfig.from_env()
