from dataclasses import dataclass, asdict
import json


@dataclass
class CheckResult:
    """ Dataclass containing check results """

    # Check results
    success: bool
    response_code: str
    response_length: int
    response_time: float
    datetime: str

    # Request parameters
    url: str
    expected_code: int = 200
    regexp: str = None

    def dumps(self):
        """ Convert self to bytes """
        return json.dumps(asdict(self)).encode("utf-8")

    @classmethod
    def loads(cls, string):
        """ Restore object from bytes """
        data = json.loads(string.decode("utf-8"))
        return cls(**data)