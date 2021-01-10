from monitoring.kafka import CheckResult, KafkaReceiver
from monitoring.db import DB

print("Consumer started")
model = DB()
print("DB connected")
receiver = KafkaReceiver()
print("Kafka connected")

print("=== Waiting for new results ===")
for result in receiver.receive():
    print(result)
    model.add_check_result(result)
