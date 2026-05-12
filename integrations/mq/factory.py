from core.config import get_settings
from integrations.mq.ports import MQProducer
from integrations.mq.rabbitmq.producer import RabbitMQProducer
from integrations.mq.rocketmq.producer import RocketMQProducer


def get_mq_producer() -> MQProducer:
    settings = get_settings()
    if settings.mq_backend.lower() == "rocketmq":
        return RocketMQProducer()
    return RabbitMQProducer()
