import time
from monitoring.kafka import KafkaSender
from monitoring.checker import Checker

print("Checker started")
checker = Checker(sender=KafkaSender)

while True:
    checker.run()
    time.sleep(60)