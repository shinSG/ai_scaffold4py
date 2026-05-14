import pytest

from agent_scaffold.infra.vectorstore.memory_store import InMemoryVectorStore
from agent_scaffold.infra.vectorstore.ports import Document


@pytest.mark.asyncio
async def test_memory_vector_store_add_and_count() -> None:
    store = InMemoryVectorStore()
    docs = [Document(content="hello", embedding=[1.0, 0.0, 0.0]), Document(content="world", embedding=[0.0, 1.0, 0.0])]
    ids = await store.add(docs)
    assert len(ids) == 2
    assert await store.count() == 2


@pytest.mark.asyncio
async def test_memory_vector_store_search() -> None:
    store = InMemoryVectorStore()
    docs = [
        Document(content="hello", embedding=[1.0, 0.0, 0.0]),
        Document(content="world", embedding=[0.0, 1.0, 0.0]),
        Document(content="test", embedding=[0.0, 0.0, 1.0]),
    ]
    await store.add(docs)
    results = await store.search([1.0, 0.0, 0.0], top_k=2)
    assert len(results) == 2
    assert results[0].document.content == "hello"
    assert results[0].score > results[1].score


@pytest.mark.asyncio
async def test_memory_vector_store_delete() -> None:
    store = InMemoryVectorStore()
    docs = [Document(content="hello", embedding=[1.0])]
    ids = await store.add(docs)
    assert await store.count() == 1
    await store.delete(ids)
    assert await store.count() == 0


@pytest.mark.asyncio
async def test_memory_vector_store_empty_search() -> None:
    store = InMemoryVectorStore()
    results = await store.search([1.0, 0.0], top_k=5)
    assert results == []
