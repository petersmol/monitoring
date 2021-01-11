import json
from pydantic import BaseModel


class CheckParams(BaseModel):
    """ Class containing check paarams """

    url: str
    expected_code: int = 200
    regexp: str = ""
    check_period: int = 60

    @property
    def key(self):
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
        return json.dumps(self.dict()).encode("utf-8")

    @classmethod
    def loads(cls, string):
        """ Restore object from bytes """
        data = json.loads(string.decode("utf-8"))
        return cls(**data)