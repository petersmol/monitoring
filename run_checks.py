from monitoring.kafka import KafkaSender
from monitoring.checker import Checker

checker = Checker(sender=KafkaSender)
checker.run()