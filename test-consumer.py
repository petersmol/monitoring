from monitoring.kafka import CheckResult, KafkaReceiver


receiver = KafkaReceiver()
for check in receiver.receive():
    print(check)
