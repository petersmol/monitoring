"""
run_consumer.py
~~~~~~~~~~~~~~

DB writer entry point, waits for any new messages from Kafka in the blocking mode.

"""

import logging
from monitoring.kafka import CheckResult, KafkaReceiver
from monitoring.db import DB

logging.basicConfig()
logger = logging.getLogger("consumer")
logger.setLevel("DEBUG")

logger.debug("Consumer started")
model = DB()
logger.debug("DB connected")
receiver = KafkaReceiver()
logger.debug("Kafka connected")

logger.info("Waiting for the results")
for result in receiver.receive():
    logger.info(result)
    model.add_check_result(result)
