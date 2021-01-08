# Monitoring

My system monitors website availability over the network, produces metrics about this and passes these events through an Aiven Kafka instance into an Aiven PostgreSQL database.

## Prerequisites

* Python 3.8
* Kafka 12.4
* PostgreSQL 12

## Installing

* Copy `config/config.example.yaml` to `config/config.yaml` and fill the nessesary connection parameters
* Download Kafka's `ca.pem`, `service.cert` and `service.key` to `config/` folder

## Components

### Website checker

Kafka producer which periodically checks the target websites and sends the check results to a Kafka topic.
The website checker performs the checks periodically and collect the HTTP response time, error code returned, as well as optionally checking the returned page contents for a regexp pattern that is expected to be found on the
page.

### DB writer

Kafka consumer stores the data to an PostgreSQL database.


## Contact

If you want to contact me you can reach me at <pub@petersmol.ru>