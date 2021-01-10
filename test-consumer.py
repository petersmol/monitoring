from monitoring.kafka import CheckResult, KafkaReceiver
from monitoring.db import DB

model = DB()

print("=== Checks ===")
checks = model.enumerate_checks()
for c in checks:
    print(dict(c))
print("=== Results ===")
results = model.enumerate_results()
for r in results:
    print(r)

print(f"{len(checks)} checks, {len(results)} results found")

print("=== Waiting for new results ===")
receiver = KafkaReceiver()
for result in receiver.receive():
    print(result)
    model.add_check_result(result)
