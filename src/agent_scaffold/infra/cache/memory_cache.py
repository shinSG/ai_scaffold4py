import time
from dataclasses import dataclass
from typing import Any

from agent_scaffold.infra.cache.ports import CachePort


@dataclass
class _CacheEntry:
    value: Any
    expires_at: float | None = None


class InMemoryCache(CachePort):
    def __init__(self) -> None:
        self._store: dict[str, _CacheEntry] = {}

    async def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        if entry.expires_at and time.time() > entry.expires_at:
            del self._store[key]
            return None
        return entry.value

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        expires_at = time.time() + ttl if ttl else None
        self._store[key] = _CacheEntry(value=value, expires_at=expires_at)

    async def delete(self, key: str) -> None:
        self._store.pop(key, None)

    async def exists(self, key: str) -> bool:
        entry = self._store.get(key)
        if entry is None:
            return False
        if entry.expires_at and time.time() > entry.expires_at:
            del self._store[key]
            return False
        return True

    async def clear(self) -> None:
        self._store.clear()
