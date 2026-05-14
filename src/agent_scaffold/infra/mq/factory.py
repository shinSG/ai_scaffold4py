from agent_scaffold.core.config import get_settings
from agent_scaffold.infra.mq.ports import MQProducer
from agent_scaffold.infra.mq.rabbitmq.producer import RabbitMQProducer
from agent_scaffold.infra.mq.rocketmq.producer import RocketMQProducer


def get_mq_producer() -> MQProducer:
    settings = get_settings()
    if settings.mq_backend.lower() == "rocketmq":
        return RocketMQProducer()
    return RabbitMQProducer()
