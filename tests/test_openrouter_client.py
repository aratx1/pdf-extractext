"""Tests del cliente de OpenRouter.

No hacen peticiones reales: se sustituye el transporte de httpx por uno simulado.
"""

import json

import httpx
import pytest

from app.core import get_settings
from app.infrastructure.external import openrouter_client as module
from app.infrastructure.external.openrouter_client import (
    MissingAPIKeyError,
    OpenRouterAIProvider,
    OpenRouterError,
)


@pytest.fixture(autouse=True)
def settings_limpias(monkeypatch):
    """Aísla los tests del .env real del desarrollador."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test")
    monkeypatch.setenv("OPENROUTER_MODEL", "modelo/test")
    monkeypatch.setenv("OPENROUTER_API_URL", "https://openrouter.test/api/v1")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def mock_transport(monkeypatch):
    """Sustituye httpx.AsyncClient por uno con transporte simulado.

    Devuelve una función a la que se le pasa el handler de la respuesta y que
    entrega la lista donde se van registrando las peticiones capturadas.
    """

    real_async_client = httpx.AsyncClient

    def install(handler):
        requests: list[httpx.Request] = []

        def capturing_handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return handler(request)

        def factory(*args, **kwargs):
            return real_async_client(
                transport=httpx.MockTransport(capturing_handler)
            )

        monkeypatch.setattr(module.httpx, "AsyncClient", factory)
        return requests

    return install


def respuesta_ok(content: str = "Un resumen", tokens: int = 123):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "choices": [{"message": {"content": content}}],
                "usage": {"total_tokens": tokens},
            },
        )

    return handler


async def test_sin_api_key_lanza_error_especifico(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "")
    get_settings.cache_clear()

    provider = OpenRouterAIProvider()

    with pytest.raises(MissingAPIKeyError):
        await provider.generate_summary("texto")

    get_settings.cache_clear()


async def test_una_api_key_en_blanco_tambien_lanza_error(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "   ")
    get_settings.cache_clear()

    provider = OpenRouterAIProvider()

    with pytest.raises(MissingAPIKeyError):
        await provider.generate_summary("texto")

    get_settings.cache_clear()


async def test_devuelve_el_contenido_del_modelo(mock_transport):
    mock_transport(respuesta_ok(content="Este es el resumen"))

    result = await OpenRouterAIProvider().generate_summary("texto")

    assert result.content == "Este es el resumen"


async def test_devuelve_el_modelo_configurado(mock_transport):
    mock_transport(respuesta_ok())

    result = await OpenRouterAIProvider().generate_summary("texto")

    assert result.model == "modelo/test"


async def test_devuelve_los_tokens_consumidos(mock_transport):
    mock_transport(respuesta_ok(tokens=999))

    result = await OpenRouterAIProvider().generate_summary("texto")

    assert result.tokens_used == 999


async def test_tokens_es_none_si_la_respuesta_no_los_trae(mock_transport):
    def handler(request):
        return httpx.Response(200, json={"choices": [{"message": {"content": "x"}}]})

    mock_transport(handler)

    result = await OpenRouterAIProvider().generate_summary("texto")

    assert result.tokens_used is None


async def test_una_respuesta_con_error_lanza_openrouter_error(mock_transport):
    def handler(request):
        return httpx.Response(200, json={"error": {"message": "Sin saldo"}})

    mock_transport(handler)

    with pytest.raises(OpenRouterError, match="Sin saldo"):
        await OpenRouterAIProvider().generate_summary("texto")


async def test_una_respuesta_sin_choices_lanza_openrouter_error(mock_transport):
    def handler(request):
        return httpx.Response(200, json={"algo": "inesperado"})

    mock_transport(handler)

    with pytest.raises(OpenRouterError):
        await OpenRouterAIProvider().generate_summary("texto")


async def test_una_lista_de_choices_vacia_lanza_openrouter_error(mock_transport):
    def handler(request):
        return httpx.Response(200, json={"choices": []})

    mock_transport(handler)

    with pytest.raises(OpenRouterError):
        await OpenRouterAIProvider().generate_summary("texto")


async def test_un_error_http_se_propaga(mock_transport):
    def handler(request):
        return httpx.Response(401, json={"detail": "no autorizado"})

    mock_transport(handler)

    with pytest.raises(httpx.HTTPStatusError):
        await OpenRouterAIProvider().generate_summary("texto")


async def test_envia_la_api_key_en_la_cabecera(mock_transport):
    requests = mock_transport(respuesta_ok())

    await OpenRouterAIProvider().generate_summary("texto")

    assert requests[0].headers["Authorization"] == "Bearer sk-or-test"


async def test_llama_al_endpoint_de_chat_completions(mock_transport):
    requests = mock_transport(respuesta_ok())

    await OpenRouterAIProvider().generate_summary("texto")

    assert str(requests[0].url) == "https://openrouter.test/api/v1/chat/completions"


async def test_el_prompt_incluye_el_texto_y_el_limite_de_palabras(mock_transport):
    requests = mock_transport(respuesta_ok())

    await OpenRouterAIProvider().generate_summary("el contenido del pdf", max_length=250)

    body = requests[0].read().decode()
    assert "el contenido del pdf" in body
    assert "250" in body


async def test_usa_el_modelo_configurado_en_la_peticion(mock_transport):
    requests = mock_transport(respuesta_ok())

    await OpenRouterAIProvider().generate_summary("texto")

    assert json.loads(requests[0].read())["model"] == "modelo/test"


async def test_la_api_key_explicita_tiene_prioridad_sobre_la_configuracion():
    provider = OpenRouterAIProvider(api_key="sk-or-explicita")

    assert provider._api_key == "sk-or-explicita"
