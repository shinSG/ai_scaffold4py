from typing import Any

import httpx

from core.config import Settings
from integrations.llm.ports import LLMProvider


class OllamaProvider(LLMProvider):
    name = "ollama"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._base_url = (settings.llm_base_url or "http://127.0.0.1:11434").rstrip("/")

    async def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        payload: dict[str, Any] = {
            "model": self._settings.llm_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self._settings.llm_temperature,
                "top_p": self._settings.llm_top_p,
                "num_predict": self._settings.llm_max_tokens,
            },
        }
        if self._settings.llm_top_k > 0:
            payload["options"]["top_k"] = self._settings.llm_top_k
        if system_prompt:
            payload["system"] = system_prompt
        if metadata and isinstance(metadata.get("llm_extra"), dict):
            payload.update(metadata["llm_extra"])

        async with httpx.AsyncClient(timeout=self._settings.llm_timeout_seconds) as client:
            response = await client.post(f"{self._base_url}/api/generate", json=payload)
            response.raise_for_status()

        data = response.json()
        return data.get("response", "")