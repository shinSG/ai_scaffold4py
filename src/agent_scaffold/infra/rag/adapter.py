from typing import Any

from agent_scaffold.infra.embedding.ports import EmbeddingProvider
from agent_scaffold.infra.rag.ports import RAGPort, RAGResult
from agent_scaffold.infra.vectorstore.ports import Document, VectorStore


class RAGAdapter(RAGPort):
    def __init__(self, embedding: EmbeddingProvider, vector_store: VectorStore) -> None:
        self._embedding = embedding
        self._vector_store = vector_store

    async def retrieve(self, query: str, top_k: int = 5) -> list[RAGResult]:
        query_embedding = await self._embedding.embed_query(query)
        results = await self._vector_store.search(query_embedding, top_k=top_k)
        return [
            RAGResult(
                content=result.document.content,
                score=result.score,
                metadata=result.document.metadata,
            )
            for result in results
        ]

    async def index(self, texts: list[str], metadata: list[dict[str, Any]] | None = None) -> None:
        embeddings = await self._embedding.embed(texts)
        documents = [
            Document(
                content=text,
                embedding=emb,
                metadata=meta or {},
            )
            for text, emb, meta in zip(texts, embeddings, metadata or [{}] * len(texts), strict=False)
        ]
        await self._vector_store.add(documents)
