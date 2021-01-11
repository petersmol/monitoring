"""
monitoring.kafka
~~~~~~~~~~~~~~~~~~

Module responsible for all interactions with Kafka.

"""
from dataclasses import dataclass, asdict
import kafka
from monitoring.check_models import CheckResult
from monitoring.settings import cfg


class KafkaSender:
    """
    Incapsulates Kafka producer into abstract interface.

    sender = KafkaSender()
    sender.send(check)

    """

    def __init__(self):
        def _serializer(value):
            return value.dumps()

        self.producer = kafka.KafkaProducer(
            **cfg["kafka"]["connect"], value_serializer=_serializer
        )

    def send(self, message: CheckResult):
        self.producer.send(cfg["kafka"]["topic"], message)
        self.producer.flush()


class KafkaReceiver:
    """
    Incapsulates Kafka consumer into abstract interface.

    receiver = KafkaReceiver()
    for check in receiver.receive():
        print(check)
    """

    def __init__(self):
        def _deserializer(value):
            return CheckResult.loads(value)

        self.consumer = kafka.KafkaConsumer(
            cfg["kafka"]["topic"],
            **cfg["kafka"]["connect"],
            auto_offset_reset="earliest",
            client_id="demo-client-1",
            group_id="demo-group",
            value_deserializer=_deserializer,
        )

    def receive(self):
        for message in self.consumer:
            yield message.value
