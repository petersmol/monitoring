import json
from pydantic import BaseModel


class CheckResult(BaseModel):
    """ Dataclass containing check results """

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