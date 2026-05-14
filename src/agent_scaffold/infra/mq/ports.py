from abc import ABC, abstractmethod


class MQProducer(ABC):
    @abstractmethod
    async def publish(self, topic: str, message: str) -> None:
        raise NotImplementedError


class MQConsumer(ABC):
    @abstractmethod
    async def subscribe(self, topic: str) -> None:
        raise NotImplementedError
