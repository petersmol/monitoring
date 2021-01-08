"""
monitoring.kafka
~~~~~~~~~~~~~~~~~~

Module responsible for interactions with Kafka
"""
from dataclasses import dataclass
from monitoring.settings import cfg
from kafka import KafkaConsumer, KafkaProducer


@dataclass
class CheckResult:
    """ Class containing check results """

    success: bool
    response_code: str
    response_content: str
    response_time: float
    regexp: str = None


class KafkaSender:
    def __init__(self):
        self.producer = KafkaProducer(**cfg["kafka"]["connect"])

    def send(self, message: CheckResult):
        self.producer.send(cfg["kafka"]["topic"], str(message).encode("utf-8"))
        self.producer.flush()
