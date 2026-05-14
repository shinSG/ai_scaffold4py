from agent_scaffold.infra.embedding.local_provider import LocalEmbeddingProvider
from agent_scaffold.infra.rag.adapter import RAGAdapter
from agent_scaffold.infra.vectorstore.memory_store import InMemoryVectorStore


def get_stub_retriever() -> RAGAdapter:
    return RAGAdapter(
        embedding=LocalEmbeddingProvider(),
        vector_store=InMemoryVectorStore(),
    )
