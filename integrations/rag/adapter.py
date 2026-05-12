from integrations.rag.ports import RAGPort


class RAGAdapter(RAGPort):
    async def retrieve(self, query: str) -> list[str]:
        return [f"stub context for: {query}"]
