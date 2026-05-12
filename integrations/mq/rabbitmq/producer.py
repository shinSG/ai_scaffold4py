import logging

from integrations.mq.ports import MQProducer


class RabbitMQProducer(MQProducer):
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    async def publish(self, topic: str, message: str) -> None:
        self._logger.info("rabbitmq publish topic=%s message=%s", topic, message)
