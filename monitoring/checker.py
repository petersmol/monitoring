"""
monitoring.checker
~~~~~~~~~~~~~~~~~~

Checker class is responsible for performing website checks.
"""
import logging
import requests
from time import time
from datetime import datetime
from monitoring.check_result import CheckResult

# Enable logging
# TODO: set all parameters in config-file
logging.basicConfig()
logger = logging.getLogger("checker")
logger.setLevel("DEBUG")


class Checker:
    def __init__(self, sender):
        self.sender = sender()

    def run(self):
        """ Performs all scheduled checks """
        logger.info("Checker started")
        for check_params in self.get_check_list():
            check = self.perform_check(check_params)
            self.sender.send(check)
        logger.info("Checker finished")

    def get_check_list(self):
        # TODO: get check list from DB
        return [
            {"url": "http://petersmol.ru/", "expected_code": 302},
            {
                "url": "https://aiven.io/",
            },
        ]

    def perform_check(self, check_params):
        # Making request
        logger.debug(f"Perform check {check_params}")
        start = time()
        r = requests.get(check_params["url"], allow_redirects=False)
        response_time = round(time() - start, 3)
        response_length = len(r.content)
        logger.debug(
            f"Received result in {response_time}s. Code {r.status_code}, {response_length} bytes"
        )

        # Checking if it is successful
        success = False
        expected_code = check_params.get("expected_code", 200)
        if check_params.get("regexp"):
            logger.debug(f"Checking regexp: {check_params['regexp']}")
            success = False
        else:
            if r.status_code == expected_code:
                success = True
        logger.debug(f"Success: {success}")

        # Reporting
        return CheckResult(
            success=success,
            response_code=r.status_code,
            response_length=response_length,
            response_time=response_time,
            url=check_params["url"],
            expected_code=expected_code,
            regexp=check_params.get("regexp", None),
            datetime=str(datetime.now()),
        )