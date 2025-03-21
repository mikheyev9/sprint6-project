from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable as KafkaError
from src.core.config import kafka_settings
from src.utils.backoff import backoff


class KafkaManager:
    def __init__(self):
        self.producer = None

    @backoff(KafkaError)
    def setup(self):
        """Создаём KafkaProducer при старте приложения."""
        self.producer = KafkaProducer(bootstrap_servers=[kafka_settings.dsn])

    def send(self, topic: str, value: bytes, key: bytes = None):
        """Отправляем сообщение через KafkaProducer."""
        return self.producer.send(topic=topic, value=value, key=key)

    def close(self):
        """Закрываем KafkaProducer при завершении работы."""
        if self.producer:
            self.producer.close()


kafka_producer = KafkaManager()
