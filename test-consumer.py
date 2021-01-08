from kafka import KafkaConsumer
from monitoring.settings import cfg

consumer = KafkaConsumer(
    cfg["kafka"]["topic"],
    **cfg["kafka"]["connect"],
    auto_offset_reset="earliest",
    client_id="demo-client-1",
    group_id="demo-group",
)

print("Consumer is ready")
for msg in consumer:
    print(msg)
