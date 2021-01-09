"""
monitoring.kafka
~~~~~~~~~~~~~~~~~~

Module responsible for all interactions with Kafka.

"""
from dataclasses import dataclass, asdict
import json
from kafka import KafkaConsumer, KafkaProducer
from monitoring.settings import cfg


@dataclass
class CheckResult:
    """ Dataclass containing check results """

    success: bool
    response_code: str
    response_content: str
    response_time: float
    regexp: str = None


class KafkaSender:
    """
    Incapsulates Kafka producer into abstract interface.

    sender = KafkaSender()
    sender.send(check)

    """

    def __init__(self):
        def _serializer(value):
            return json.dumps(asdict(value)).encode("utf-8")

        self.producer = KafkaProducer(
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
            data = json.loads(value.decode("utf-8"))
            return CheckResult(**data)

        self.consumer = KafkaConsumer(
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
