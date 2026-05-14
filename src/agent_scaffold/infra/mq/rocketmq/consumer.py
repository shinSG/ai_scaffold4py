import logging

from agent_scaffold.infra.mq.ports import MQConsumer


class RocketMQConsumer(MQConsumer):
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    async def subscribe(self, topic: str) -> None:
        self._logger.info("rocketmq subscribe topic=%s", topic)
