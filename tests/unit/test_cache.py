import pytest

from agent_scaffold.infra.cache.memory_cache import InMemoryCache


@pytest.mark.asyncio
async def test_memory_cache_set_and_get() -> None:
    cache = InMemoryCache()
    await cache.set("key1", "value1")
    assert await cache.get("key1") == "value1"


@pytest.mark.asyncio
async def test_memory_cache_get_missing() -> None:
    cache = InMemoryCache()
    assert await cache.get("nonexistent") is None


@pytest.mark.asyncio
async def test_memory_cache_delete() -> None:
    cache = InMemoryCache()
    await cache.set("key1", "value1")
    await cache.delete("key1")
    assert await cache.get("key1") is None


@pytest.mark.asyncio
async def test_memory_cache_exists() -> None:
    cache = InMemoryCache()
    assert await cache.exists("key1") is False
    await cache.set("key1", "value1")
    assert await cache.exists("key1") is True


@pytest.mark.asyncio
async def test_memory_cache_clear() -> None:
    cache = InMemoryCache()
    await cache.set("key1", "value1")
    await cache.set("key2", "value2")
    await cache.clear()
    assert await cache.exists("key1") is False
    assert await cache.exists("key2") is False


@pytest.mark.asyncio
async def test_memory_cache_ttl() -> None:
    cache = InMemoryCache()
    await cache.set("key1", "value1", ttl=1)
    assert await cache.get("key1") == "value1"


@pytest.mark.asyncio
async def test_memory_cache_dict_value() -> None:
    cache = InMemoryCache()
    await cache.set("key1", {"nested": "data"})
    assert await cache.get("key1") == {"nested": "data"}
