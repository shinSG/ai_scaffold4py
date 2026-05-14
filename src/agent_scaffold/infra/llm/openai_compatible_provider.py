from typing import Any

import httpx

from agent_scaffold.core.config import Settings
from agent_scaffold.core.exceptions import ConfigurationError
from agent_scaffold.infra.llm.ports import LLMProvider


class OpenAICompatibleProvider(LLMProvider):
    name = "openai-compatible"

    def __init__(self, settings: Settings, *, base_url: str | None = None) -> None:
        self._settings = settings
        self._base_url = (base_url or settings.llm_base_url or "https://api.openai.com/v1").rstrip("/")

    async def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        if not self._settings.llm_api_key:
            raise ConfigurationError("LLM_API_KEY is required for OpenAI-compatible providers")

        runtime_options = self._get_runtime_options(metadata)
        payload = self._build_payload(prompt, system_prompt=system_prompt, metadata=metadata)

        headers = {"Authorization": f"Bearer {self._settings.llm_api_key}"}
        async with httpx.AsyncClient(timeout=self._settings.llm_timeout_seconds) as client:
            response = await client.post(f"{self._base_url}/chat/completions", json=payload, headers=headers)
            response.raise_for_status()

        return self._extract_content(response.json(), show_reasoning=runtime_options.get("show_reasoning"))

    def _build_payload(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        runtime_options = self._get_runtime_options(metadata)
        model = runtime_options.get("model", self._settings.llm_model)
        temperature = runtime_options.get("temperature", self._settings.llm_temperature)
        top_p = runtime_options.get("top_p", self._settings.llm_top_p)
        top_k = runtime_options.get("top_k", self._settings.llm_top_k)
        max_tokens = runtime_options.get("max_tokens", self._settings.llm_max_tokens)
        enable_thinking = runtime_options.get("enable_thinking", self._settings.llm_enable_thinking)

        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
        }
        if isinstance(top_k, int) and top_k > 0:
            payload["top_k"] = top_k
        if enable_thinking:
            payload["enable_thinking"] = True
        if metadata and isinstance(metadata.get("llm_extra"), dict):
            payload.update(metadata["llm_extra"])
        if isinstance(runtime_options.get("extra"), dict):
            payload.update(runtime_options["extra"])
        return payload

    def _extract_content(self, data: dict[str, Any], *, show_reasoning: bool | None = None) -> str:
        choices = data.get("choices") or []
        if not choices:
            return ""
        message = choices[0].get("message") or {}
        content = message.get("content") or choices[0].get("text") or ""
        reasoning = message.get("reasoning_content") or message.get("reasoning") or ""
        should_show_reasoning = self._settings.llm_show_reasoning if show_reasoning is None else show_reasoning
        if should_show_reasoning and reasoning:
            return f"<think>\n{reasoning}\n</think>\n\n{content}"
        return content

    def _get_runtime_options(self, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        if not metadata or not isinstance(metadata.get("llm_options"), dict):
            return {}
        return metadata["llm_options"]
