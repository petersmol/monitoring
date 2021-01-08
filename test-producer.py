from monitoring.kafka import CheckResult, KafkaSender

message = CheckResult(
    success=False,
    response_code=200,
    response_content="Hello world",
    response_time=0.010,
)
print(message)

sender = KafkaSender()
sender.send(message)