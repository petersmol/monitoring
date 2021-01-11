"""
monitoring.checker
~~~~~~~~~~~~~~~~~~

Checker class is responsible for performing website checks.
"""
import logging
import re
from redis import Redis
import pydantic
import requests
from time import time
from datetime import datetime
from monitoring.check_models import CheckParams, CheckResult
from monitoring.settings import cfg

# Enable logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class Checker:
    def __init__(self, sender):
        self.sender = sender()
        self.redis = Redis.from_url(cfg["redis_uri"])

    def run(self):
        """ Performs all scheduled checks """
        for check_params in self.get_check_list():
            # Skipping if it is too early for the next check
            if self.redis.get(check_params.key):
                continue
            check = self.perform_check(check_params)

            self.redis.set(check_params.key, 1, ex=check_params.check_period)
            self.sender.send(check)

    def get_check_list(self):
        """
        Getting the list of checks from config
        """
        return [CheckParams.parse_obj(x) for x in cfg["checks"]]

    def perform_check(self, check_params: CheckParams):
        # Making request
        logger.debug(f"Perform check {check_params}")
        start = time()
        r = requests.get(check_params.url, allow_redirects=False)
        response_time = round(time() - start, 3)
        response_length = len(r.content)
        logger.debug(
            f"Received result in {response_time}s. Code {r.status_code}, {response_length} bytes"
        )

        # Checking if it is successful
        success = False
        if check_params.regexp:
            pattern = re.compile(check_params.regexp)
            success = bool(pattern.search(r.content))
            logger.debug(f"Checking regexp {pattern}. Success: {success}")
        else:
            if r.status_code == check_params.expected_code:
                success = True
            logger.debug(
                f"Code {r.status_code}, expected: {check_params.expected_code}. Success: {success}"
            )

        # Reporting
        return CheckResult(
            success=success,
            response_code=r.status_code,
            response_length=response_length,
            response_time=response_time,
            url=check_params.url,
            expected_code=check_params.expected_code,
            regexp=check_params.regexp,
            created=str(datetime.now()),
        )