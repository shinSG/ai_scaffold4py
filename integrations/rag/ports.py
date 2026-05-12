from abc import ABC, abstractmethod


class RAGPort(ABC):
    @abstractmethod
    async def retrieve(self, query: str) -> list[str]:
        raise NotImplementedError
