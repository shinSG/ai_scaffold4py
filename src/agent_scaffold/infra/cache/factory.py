from agent_scaffold.core.config import get_settings
from agent_scaffold.infra.cache.ports import CachePort


def get_cache() -> CachePort:
    settings = get_settings()
    backend = settings.cache_backend.lower()

    if backend == "redis":
        from agent_scaffold.infra.cache.redis_cache import RedisCache
        return RedisCache(settings)

    from agent_scaffold.infra.cache.memory_cache import InMemoryCache
    return InMemoryCache()
