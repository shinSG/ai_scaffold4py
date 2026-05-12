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
        runtime_options = self._get_runtime_options(metadata)
        model = runtime_options.get("model", self._settings.llm_model)
        temperature = runtime_options.get("temperature", self._settings.llm_temperature)
        top_p = runtime_options.get("top_p", self._settings.llm_top_p)
        top_k = runtime_options.get("top_k", self._settings.llm_top_k)
        max_tokens = runtime_options.get("max_tokens", self._settings.llm_max_tokens)

        payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": top_p,
                "num_predict": max_tokens,
            },
        }
        if isinstance(top_k, int) and top_k > 0:
            payload["options"]["top_k"] = top_k
        if system_prompt:
            payload["system"] = system_prompt
        if metadata and isinstance(metadata.get("llm_extra"), dict):
            payload.update(metadata["llm_extra"])
        if isinstance(runtime_options.get("extra"), dict):
            payload.update(runtime_options["extra"])

        async with httpx.AsyncClient(timeout=self._settings.llm_timeout_seconds) as client:
            response = await client.post(f"{self._base_url}/api/generate", json=payload)
            response.raise_for_status()

        data = response.json()
        return data.get("response", "")

    def _get_runtime_options(self, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        if not metadata or not isinstance(metadata.get("llm_options"), dict):
            return {}
        return metadata["llm_options"]