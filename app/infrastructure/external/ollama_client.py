import httpx
from app.application.interfaces.ai_provider import AIProvider, AIResponse
from app.core import get_settings


class OllamaAIProvider(AIProvider):
    def __init__(self, base_url: str | None = None, model: str | None = None):
        settings = get_settings()
        self._base_url = (base_url or settings.ollama_base_url).rstrip("/")
        self._model = model or settings.ollama_model

    async def generate_summary(self, text: str, max_length: int = 500) -> AIResponse:
        prompt = self._build_summary_prompt(text, max_length)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/api/chat",
                json={
                    "model": self._model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "Eres un asistente experto en síntesis de información. Resume el siguiente texto de forma clara y concisa, en el mismo idioma en que está escrito. No agregues información que no esté en el texto original.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 1024,
                    },
                },
                timeout=120.0,
            )
            response.raise_for_status()
            data = response.json()

            return AIResponse(
                content=data["message"]["content"],
                model=self._model,
            )

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self._base_url}/api/tags", timeout=5.0)
                return response.status_code == 200
        except httpx.RequestError:
            return False

    def _build_summary_prompt(self, text: str, max_length: int) -> str:
        return (
            f"Por favor, proporciona un resumen conciso del siguiente documento "
            f"(máximo {max_length} palabras):\n\n{text}"
        )
