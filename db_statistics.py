from monitoring.kafka import CheckResult, KafkaReceiver
from monitoring.db import DB
import logging

logging.basicConfig()
logger = logging.getLogger("statistics")
logger.setLevel("DEBUG")

model = DB()

logger.info("=== Checks ===")
checks = model.enumerate_checks()
for c in checks:
    logger.info(dict(c))
logger.info("=== Results ===")
results = model.enumerate_results()
for r in results:
    logger.info(r)

logger.info(f"{len(checks)} checks, {len(results)} results found")
