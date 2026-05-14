import json
from typing import Any

from agent_scaffold.core.config import Settings
from agent_scaffold.infra.cache.ports import CachePort


class RedisCache(CachePort):
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = None

    def _ensure_client(self) -> None:
        if self._client is None:
            import redis.asyncio as redis
            self._client = redis.from_url(self._settings.cache_redis_url, decode_responses=True)

    async def get(self, key: str) -> Any | None:
        self._ensure_client()
        value = await self._client.get(key)  # type: ignore[union-attr]
        if value is None:
            return None
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        self._ensure_client()
        serialized = json.dumps(value) if not isinstance(value, str) else value
        if ttl:
            await self._client.setex(key, ttl, serialized)  # type: ignore[union-attr]
        else:
            await self._client.set(key, serialized)  # type: ignore[union-attr]

    async def delete(self, key: str) -> None:
        self._ensure_client()
        await self._client.delete(key)  # type: ignore[union-attr]

    async def exists(self, key: str) -> bool:
        self._ensure_client()
        return bool(await self._client.exists(key))  # type: ignore[union-attr]

    async def clear(self) -> None:
        self._ensure_client()
        await self._client.flushdb()  # type: ignore[union-attr]
