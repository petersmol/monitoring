"""
run_checker.py
~~~~~~~~~~~~~~

Website checker entry point, runs all checks in the loop.
Check period is stored in the config and taken into account inside the Checker()
"""

import time
from monitoring.kafka import KafkaSender
from monitoring.checker import Checker

checker = Checker(sender=KafkaSender)

while True:
    checker.run()
    time.sleep(1)