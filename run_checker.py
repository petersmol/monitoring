import time
from monitoring.kafka import KafkaSender
from monitoring.checker import Checker

checker = Checker(sender=KafkaSender)

while True:
    checker.run()
    time.sleep(60)