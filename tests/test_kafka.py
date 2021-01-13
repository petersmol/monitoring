import pytest
from monitoring.settings import cfg
import monitoring.kafka
import kafka
from unittest.mock import MagicMock


def test_sender(mocker):
    mocker.patch("kafka.KafkaProducer")

    # Creating Sender object
    sender = monitoring.kafka.KafkaSender()
    sender.send("dummy")
    sender.producer.send.assert_called_once_with(cfg["kafka"]["topic"], "dummy")
    sender.producer.flush.assert_called_once_with()


def test_receiver(mocker):
    mocker.patch("kafka.KafkaConsumer", return_value=[])

    # Creating Sender object
    receiver = monitoring.kafka.KafkaReceiver()
    receiver.receive()
