import math
from uuid import uuid4

from agent_scaffold.infra.vectorstore.ports import Document, SearchResult, VectorStore


class InMemoryVectorStore(VectorStore):
    def __init__(self) -> None:
        self._documents: dict[str, Document] = {}

    async def add(self, documents: list[Document]) -> list[str]:
        ids = []
        for doc in documents:
            doc_id = doc.id or str(uuid4())
            doc.id = doc_id
            self._documents[doc_id] = doc
            ids.append(doc_id)
        return ids

    async def search(self, query_embedding: list[float], top_k: int = 5) -> list[SearchResult]:
        if not self._documents:
            return []

        scored: list[SearchResult] = []
        for doc in self._documents.values():
            if doc.embedding:
                score = self._cosine_similarity(query_embedding, doc.embedding)
                scored.append(SearchResult(document=doc, score=score))

        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:top_k]

    async def delete(self, ids: list[str]) -> None:
        for doc_id in ids:
            self._documents.pop(doc_id, None)

    async def count(self) -> int:
        return len(self._documents)

    @staticmethod
    def _cosine_similarity(a: list[float], b: list[float]) -> float:
        if len(a) != len(b):
            return 0.0
        dot = sum(x * y for x, y in zip(a, b, strict=False))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)
