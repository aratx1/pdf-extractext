"""OpenRouter API client - OpenAI-compatible API implementation."""

import httpx
from app.application.interfaces.ai_provider import AIProvider, AIResponse
from app.core import get_settings


class OpenRouterAIProvider(AIProvider):
    def __init__(self, api_key: str | None = None):
        settings = get_settings()
        self._api_key = api_key or settings.openrouter_api_key
        self._base_url = settings.openrouter_api_url
        self._model = settings.openrouter_model

    async def generate_summary(self, text: str, max_length: int = 500) -> AIResponse:
        prompt = self._build_summary_prompt(text, max_length)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:8000",
                },
                json={
                    "model": self._model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "Eres un asistente experto en síntesis de información. Resume el siguiente texto de forma clara y concisa, en el mismo idioma en que está escrito. No agregues información que no esté en el texto original.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "max_tokens": 1024,
                    "temperature": 0.3,
                },
                timeout=60.0,
            )
            response.raise_for_status()
            data = response.json()

            return AIResponse(
                content=data["choices"][0]["message"]["content"],
                model=self._model,
                tokens_used=data.get("usage", {}).get("total_tokens"),
            )

    async def health_check(self) -> bool:
        return True

    def _build_summary_prompt(self, text: str, max_length: int) -> str:
        return (
            f"Por favor, proporciona un resumen conciso del siguiente documento "
            f"(máximo {max_length} palabras):\n\n{text}"
        )
