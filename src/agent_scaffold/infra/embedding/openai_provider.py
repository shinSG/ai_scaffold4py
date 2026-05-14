from typing import Any

import httpx

from agent_scaffold.core.config import Settings
from agent_scaffold.core.exceptions import ConfigurationError
from agent_scaffold.infra.embedding.ports import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):
    name = "openai"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._base_url = (settings.embedding_base_url or "https://api.openai.com/v1").rstrip("/")
        self._model = settings.embedding_model
        self._dim: int = 0

    @property
    def dimension(self) -> int:
        return self._dim

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if not self._settings.llm_api_key:
            raise ConfigurationError("LLM_API_KEY is required for OpenAI embedding provider")

        headers = {"Authorization": f"Bearer {self._settings.llm_api_key}"}
        payload = {"model": self._model, "input": texts}

        async with httpx.AsyncClient(timeout=self._settings.llm_timeout_seconds) as client:
            response = await client.post(f"{self._base_url}/embeddings", json=payload, headers=headers)
            response.raise_for_status()

        data = response.json()
        embeddings = [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]
        if embeddings and not self._dim:
            self._dim = len(embeddings[0])
        return embeddings

    async def embed_query(self, text: str) -> list[float]:
        results = await self.embed([text])
        return results[0]
