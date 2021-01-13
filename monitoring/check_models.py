"""
check_models.py
~~~~~~~~~~~~~~~

Pydantic models to verify check parameters and check results during serialization/deserialization
"""

import json
from pydantic import BaseModel


class CheckParams(BaseModel):
    """ Class containing check params """

    url: str
    expected_code: int = 200
    regexp: str = ""
    check_period: int = 60

    @property
    def key(self):
        """ unique check identifier for redis """
        return self.url


class CheckResult(BaseModel):
    """ Class containing check results """

    # Check results
    success: bool
    response_code: str
    response_length: int
    response_time: float
    created: str

    # Request parameters
    url: str
    expected_code: int = 200
    regexp: str = ""

    def dumps(self):
        """ Convert self to bytes """
        return self.json().encode("utf-8")

    @classmethod
    def loads(cls, string):
        """ Restore object from bytes """
        return cls.parse_raw(string)