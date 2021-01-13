"""
run_checker_once.py
~~~~~~~~~~~~~~~~~~~

Like run_checker.py, but without the loop. For debugging purposes.
"""
from monitoring.kafka import KafkaSender
from monitoring.checker import Checker

checker = Checker(sender=KafkaSender)
checker.run()