import pytest

from agent_scaffold.infra.embedding.local_provider import LocalEmbeddingProvider


@pytest.mark.asyncio
async def test_local_embedding_provider_embed() -> None:
    provider = LocalEmbeddingProvider(dimension=64)
    results = await provider.embed(["hello", "world"])
    assert len(results) == 2
    assert len(results[0]) == 64
    assert len(results[1]) == 64


@pytest.mark.asyncio
async def test_local_embedding_provider_embed_query() -> None:
    provider = LocalEmbeddingProvider(dimension=64)
    result = await provider.embed_query("hello world")
    assert len(result) == 64


@pytest.mark.asyncio
async def test_local_embedding_provider_deterministic() -> None:
    provider = LocalEmbeddingProvider(dimension=64)
    r1 = await provider.embed_query("test")
    r2 = await provider.embed_query("test")
    assert r1 == r2


@pytest.mark.asyncio
async def test_local_embedding_provider_different_inputs() -> None:
    provider = LocalEmbeddingProvider(dimension=64)
    r1 = await provider.embed_query("hello")
    r2 = await provider.embed_query("world")
    assert r1 != r2


def test_local_embedding_provider_dimension() -> None:
    provider = LocalEmbeddingProvider(dimension=128)
    assert provider.dimension == 128
    assert provider.name == "local"
