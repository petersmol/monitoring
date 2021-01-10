# Monitoring

My system monitors website availability over the network and passes these events through an Aiven Kafka instance into an Aiven PostgreSQL database.

## Prerequisites

* Python 3.8
* Kafka 12.4
* PostgreSQL 12

## Installing

* Copy [config/config.example.yaml](config/config.example.yaml) to `config/config.yaml`.
* Download Kafka's `ca.pem`, `service.cert` and `service.key` to `config/` folder, fill `kafka.connect.bootstrap_servers` in config.yaml with the actual host:port.
* Add your checks to the config.yaml.
## Checks configuration

You can add an arbitrary number of checks into the config. Following parameters are accepted

| Parameter | Required | Description |
| **url** | Yes |  page to request, e.g. `https://example.com/index.html`. At the moment, only GET requests are supported. |
| **expected_code** | No, default: 200 | Which HTTP response code we're expecting (all other will be treated as failure). |
| **regexp** | No, default: "" | Check page for matching regular expression. Response code will be ignored. |

## Components

### Website checker

Kafka producer which periodically checks the target websites and sends the check results to a Kafka topic.
The website checker performs the checks periodically and collects the HTTP response time, error code returned, as well as optionally checking the returned page contents for a regexp pattern that is expected to be found on the
page.

### DB writer

Kafka consumer stores the data to the PostgreSQL database. Information is stored in 2 tables:

`checks` – information about different checks (URL, regexp, expected return code). Checks are immutable, any change will create a new one. The only mutable field is `last_check`, which is updated after each insert.

`results` - all results for a given check. Besides boolean `success` value, provides some additional data for analytics: response time in seconds, response length, returned HTTP code.


## Contact

If you want to contact me you can reach me at <pub@petersmol.ru>