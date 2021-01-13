# Monitoring

My system monitors website availability over the network and passes these events through an Aiven Kafka instance into an Aiven PostgreSQL database.

## Prerequisites

* Python 3.8
* PostgreSQL 12 - main storage
* Kafka 12.4 - message broker between checker and db-writer instances
* Redis - for tracking last check time
* Docker - not nessesary, but it's convenient for production deployment

## Running in Docker

* Download source code to your local machine (`git clone git@github.com:petersmol/monitoring.git`)
* Update the configuration file (see "Configuring" section below)
* Build the docker image:
```
docker build -t monitoring .
```
* Run consumer container:
```
docker run monitoring python -u run_consumer.py
```
* Run checker container:
```
docker run monitoring python -u run_checker.py
```

You can also use prebuilt docker image and mount your `config/` folder into `/app/config`.

## Running without docker

Download source code to your local machine
```
pip install pipenv
pipenv install
pipenv shell
```

Then in pipenv shell you can run scripts in root project folder:
* `python run_consumer.py` - start DB writer service
* `python run_checker.py` - start website checker service
* `python run_checker_once.py` - perform all checks once and exit
* `python db_statistics.py` - quick look into the existing DB entries


### Deploying to AWS Elastic Container Service
* Push builded docker image to AWS ECR following their instructions
* Create new ECS task with 2 containers `consumer` and `checker`. Use the same image for both and add custom entrypoints: `python, -u, run_consumer.py` and `python, -u, run_checker.py` accordingly.

## Configuring

Copy [config/config.example.yaml](config/config.example.yaml) to `config/config.yaml`, then follow the instructions below.

### Kafka
* Order Aiven Kafka instance and create topic.
* Download Kafka's `ca.pem`, `service.cert` and `service.key` to `config/` folder
* Fill `kafka.connect.bootstrap_servers` in config.yaml with the actual host:port
* Fill `kafka.topic` in config.yaml with topic naame.

### PostgreSQL
* Order Aiven PostgreSQL instance. You can use the default database or create new one if needed.
* Fill `postgresql_uri` in config.yaml with your database URI.

### Redis
* Fill `redis_uri` in config.yaml with your redis URI.
### Checks configuration

You can add an arbitrary number of checks into the config. Following parameters are accepted

| Parameter | Required | Description |
| --- | --- | --- |
| **url** | Yes |  page to request, e.g. `https://example.com/index.html`. At the moment, only GET requests are supported. |
| **expected_code** | No, default: 200 | Which HTTP response code we're expecting (all other will be treated as failure). |
| **regexp** | No, default: "" | Check page for matching regular expression. Response code will be ignored. |
| **check_period** | No, default: 60 | How often we want to run the check (in seconds). |



## Components

### Website checker

Checker runs all checks from the config file every 60 seconds, then sends results to the writer using Kafka producer.

### DB writer

Kafka consumer stores the data to the PostgreSQL database. Information is stored in 2 tables:

`checks` – information about different checks (URL, regexp, expected return code). Checks are immutable, any change will create a new one. The only mutable field is `last_check`, which is updated after each insert.

`results` - all results for a given check. Besides boolean `success` value, provides some additional data for analytics: response time in seconds, response length, returned HTTP code.

## Known issues
* Test coverage could be better.
## Contact

If you want to contact me you can reach me at <pub@petersmol.ru>