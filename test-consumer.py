from monitoring.kafka import CheckResult, KafkaReceiver
from monitoring.db import DB

model = DB()

all_checks = model.enumerate_check_results()

for c in all_checks:
    print(c)

print(f"{len(all_checks)} results found")

receiver = KafkaReceiver()
for result in receiver.receive():
    print(result)
    model.add_check_result(result)
