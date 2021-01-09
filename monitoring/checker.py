"""
monitoring.checker
~~~~~~~~~~~~~~~~~~

Checker class is responsible for performing website checks.
"""
import logging
import re
import requests
from time import time
from datetime import datetime
from monitoring.check_result import CheckResult
from monitoring.settings import cfg

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
        """
        Getting the list of checks from config
        """
        return cfg["checks"]

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
            pattern = re.compile(check_params["regexp"])
            success = bool(pattern.search(r.content))
            logger.debug(f"Checking regexp {pattern}. Success: {success}")
        else:
            if r.status_code == expected_code:
                success = True
            logger.debug(
                f"Code {r.status_code}, expected: {expected_code}. Success: {success}"
            )

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