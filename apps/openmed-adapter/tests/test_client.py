import httpx
import pytest

from openmed_adapter import (
    OpenMedClient,
    OpenMedConfig,
    OpenMedHTTPStatusError,
    OpenMedNetworkError,
    OpenMedTimeoutError,
)


def _client_for(handler):
    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(transport=transport, base_url="https://openmed.test")
    return OpenMedClient(OpenMedConfig(base_url="https://openmed.test"), http_client=http_client)


def test_health_check_returns_typed_payload():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/health"
        return httpx.Response(200, json={"ok": True})

    client = _client_for(handler)
    result = client.health_check()

    assert result.status_code == 200
    assert result.payload == {"ok": True}


def test_analyze_text_sends_language_when_provided():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/analyze-text"
        assert request.method == "POST"
        assert request.read() == b'{"text":"hola","language":"es"}'
        return httpx.Response(200, json={"result": "ok"})

    client = _client_for(handler)
    result = client.analyze_text("hola", language="es")

    assert result.payload == {"result": "ok"}


def test_extract_pii_without_language_omits_field():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/extract-pii"
        assert request.read() == b'{"text":"abc"}'
        return httpx.Response(200, json={"entities": []})

    client = _client_for(handler)
    result = client.extract_pii("abc")

    assert result.payload == {"entities": []}


def test_deidentify_text_falls_back_to_raw_text_if_not_json():
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="plain-text-response")

    client = _client_for(handler)
    result = client.deidentify_text("abc")

    assert result.payload == {"raw_text": "plain-text-response"}


def test_raises_http_status_error():
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="boom")

    client = _client_for(handler)

    with pytest.raises(OpenMedHTTPStatusError) as exc:
        client.health_check()

    assert exc.value.status_code == 500
    assert exc.value.response_text == "boom"


def test_raises_timeout_error():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timeout", request=request)

    client = _client_for(handler)

    with pytest.raises(OpenMedTimeoutError):
        client.health_check()


def test_raises_network_error():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("network down", request=request)

    client = _client_for(handler)

    with pytest.raises(OpenMedNetworkError):
        client.health_check()
