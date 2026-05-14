from uuid import uuid4

from agent_scaffold.core.config import Settings
from agent_scaffold.infra.vectorstore.ports import Document, SearchResult, VectorStore


class ChromaVectorStore(VectorStore):
    def __init__(self, settings: Settings, collection_name: str = "default") -> None:
        self._settings = settings
        self._collection_name = collection_name
        self._client = None
        self._collection = None

    def _ensure_client(self) -> None:
        if self._client is None:
            import chromadb
            self._client = chromadb.HttpClient(
                host=self._settings.vectorstore_endpoint.replace("http://", "").replace("https://", "").split(":")[0],
                port=int(self._settings.vectorstore_endpoint.split(":")[-1]) if ":" in self._settings.vectorstore_endpoint else 8000,
            )
            self._collection = self._client.get_or_create_collection(self._collection_name)

    async def add(self, documents: list[Document]) -> list[str]:
        self._ensure_client()
        ids = [doc.id or str(uuid4()) for doc in documents]
        self._collection.add(  # type: ignore[union-attr]
            ids=ids,
            documents=[doc.content for doc in documents],
            metadatas=[doc.metadata for doc in documents],
            embeddings=[doc.embedding for doc in documents] if documents[0].embedding else None,
        )
        return ids

    async def search(self, query_embedding: list[float], top_k: int = 5) -> list[SearchResult]:
        self._ensure_client()
        results = self._collection.query(  # type: ignore[union-attr]
            query_embeddings=[query_embedding],
            n_results=top_k,
        )
        documents = []
        for i, doc_id in enumerate(results["ids"][0]):
            doc = Document(
                id=doc_id,
                content=results["documents"][0][i],
                metadata=results["metadatas"][0][i] if results["metadatas"] else {},
            )
            score = 1.0 - results["distances"][0][i] if results.get("distances") else 0.0
            documents.append(SearchResult(document=doc, score=score))
        return documents

    async def delete(self, ids: list[str]) -> None:
        self._ensure_client()
        self._collection.delete(ids=ids)  # type: ignore[union-attr]

    async def count(self) -> int:
        self._ensure_client()
        return self._collection.count()  # type: ignore[union-attr]
