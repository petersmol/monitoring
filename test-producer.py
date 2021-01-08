import yaml
from kafka import KafkaProducer
from monitoring.settings import cfg

producer = KafkaProducer(**cfg["kafka"])

print("Producer loaded")
for i in range(4):
    message = "message number {}".format(i)
    producer.send("my_favorite_topic", message.encode("utf-8"))
    print(f"Message {i} sent")
producer.flush()
