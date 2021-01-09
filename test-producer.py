from monitoring.kafka import CheckResult, KafkaSender

check = CheckResult(
    success=False,
    response_code=200,
    response_content="Hello world",
    response_time=0.010,
)
print(check)

sender = KafkaSender()
sender.send(check)