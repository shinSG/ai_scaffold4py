from integrations.rag.adapter import RAGAdapter


def get_stub_retriever() -> RAGAdapter:
    return RAGAdapter()
