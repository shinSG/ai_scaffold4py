from agent_scaffold.core.config import get_settings
from agent_scaffold.infra.vectorstore.ports import VectorStore


def get_vector_store() -> VectorStore:
    settings = get_settings()
    backend = settings.vectorstore_backend.lower()

    if backend == "chroma":
        from agent_scaffold.infra.vectorstore.chroma_store import ChromaVectorStore
        return ChromaVectorStore(settings)

    from agent_scaffold.infra.vectorstore.memory_store import InMemoryVectorStore
    return InMemoryVectorStore()
