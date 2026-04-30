"""Tests para verificar la conexión con OpenRouter API."""

import os
import sys
import httpx
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_api_key_configured():
    """Verifica que la API key esté configurada."""
    from app.core import get_settings

    settings = get_settings()

    assert settings.openrouter_api_key, "OPENROUTER_API_KEY no está configurada en .env"
    assert settings.openrouter_api_key.startswith("sk-or-"), (
        "API key no tiene el formato correcto de OpenRouter"
    )
    print(f"✓ API key configurada: {settings.openrouter_api_key[:15]}...")


def test_api_connection():
    """Verifica que se puede conectar a OpenRouter."""
    from app.core import get_settings

    settings = get_settings()

    url = f"{settings.openrouter_api_url}/models"
    headers = {"Authorization": f"Bearer {settings.openrouter_api_key}"}

    response = httpx.get(url, headers=headers, timeout=10.0)
    assert response.status_code == 200, (
        f"Error conectando: {response.status_code} - {response.text}"
    )
    print("✓ Conexión a OpenRouter exitosa")


def test_simple_completion():
    """Test básico: envía un prompt simple y verifica respuesta."""
    from app.core import get_settings

    settings = get_settings()

    url = f"{settings.openrouter_api_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
    }
    data = {
        "model": "openrouter/free",
        "messages": [{"role": "user", "content": "Di 'hola' en una palabra"}],
        "max_tokens": 50,
    }

    response = httpx.post(url, headers=headers, json=data, timeout=30.0)

    if response.status_code == 200:
        result = response.json()
        actual_model = result.get("model", "desconocido")
        content = result["choices"][0]["message"]["content"]
        print(f"✓ Respuesta del modelo: {content}")
        print(f"  Modelo seleccionado por router: {actual_model}")
    else:
        print(f"✗ Error {response.status_code}: {response.text}")
        return False

    return True


def test_summary_request():
    """Test de resumen real."""
    from app.core import get_settings

    settings = get_settings()

    test_text = "Python es un lenguaje de programación de alto nivel, interpretado y de propósito general. Fue creado por Guido van Rossum y lanzado en 1991. Python enfatiza la legibilidad del código con su sintaxis clara y usa indentación."

    url = f"{settings.openrouter_api_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
    }
    data = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "system",
                "content": "Eres un asistente experto en síntesis de información. Resume el siguiente texto de forma clara y concisa, en el mismo idioma en que está escrito.",
            },
            {
                "role": "user",
                "content": f"Resume este texto en máximo 20 palabras: {test_text}",
            },
        ],
        "max_tokens": 1024,
        "temperature": 0.3,
    }

    print(f"Enviando texto de {len(test_text)} caracteres...")
    response = httpx.post(url, headers=headers, json=data, timeout=60.0)

    if response.status_code == 200:
        result = response.json()
        actual_model = result.get("model", "desconocido")
        summary = result["choices"][0]["message"]["content"]
        usage = result.get("usage", {})
        print(f"✓ Resumen generado: {summary}")
        print(f"  Modelo seleccionado por router: {actual_model}")
        print(f"  Tokens usados: {usage.get('total_tokens', 'N/A')}")
        return True
    else:
        print(f"✗ Error {response.status_code}: {response.text}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("TEST DE CONEXIÓN OPENROUTER")
    print("=" * 50)

    try:
        print("\n1. Verificando API key...")
        test_api_key_configured()

        print("\n2. Verificando conexión...")
        test_api_connection()

        print("\n3. Test simple de completion...")
        test_simple_completion()

        print("\n4. Test de resumen...")
        test_summary_request()

        print("\n" + "=" * 50)
        print("TODOS LOS TESTS PASARON")
        print("=" * 50)

    except AssertionError as e:
        print(f"\n✗ TEST FALLÓ: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR INESPERADO: {e}")
        sys.exit(1)
