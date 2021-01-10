# Monitoring

My system monitors website availability over the network, produces metrics about this and passes these events through an Aiven Kafka instance into an Aiven PostgreSQL database.

## Prerequisites

* Python 3.8
* Kafka 12.4
* PostgreSQL 12

## Installing

* Copy `config/config.example.yaml` to `config/config.yaml`.
* Download Kafka's `ca.pem`, `service.cert` and `service.key` to `config/` folder, fill `kafka.connect.bootstrap_servers` in config.yaml with the actual host:port.
* Fill the `checks` list in config.yaml according to your reqirements.
## Checks configuration

You can add arbitrary number of checks into the config. Following parameters are accepted

**url (required)** — page to request, e.g. `https://example.com/index.html`. At the moment, only GET requests are supported.
**expected_code** (default: 200) — which HTTP response code we're expecting (all other will be treated as failure).
**regexp** (default: None) - Check page for matching regular expression. Response code will be ignored.

## Components

### Website checker

Kafka producer which periodically checks the target websites and sends the check results to a Kafka topic.
The website checker performs the checks periodically and collect the HTTP response time, error code returned, as well as optionally checking the returned page contents for a regexp pattern that is expected to be found on the
page.

### DB writer

Kafka consumer stores the data to an PostgreSQL database.


## Contact

If you want to contact me you can reach me at <pub@petersmol.ru>