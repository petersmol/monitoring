"""
monitoring.checker
~~~~~~~~~~~~~~~~~~

Checker class is responsible for performing website checks.
"""


class Checker:
    def get_check_list(self):
        # TODO: get check list from DB
        return [{"url": "http://petersmol.ru/", "expected_code": 200, "regexp": None}]

    def perform_checks(self):
        for check in self.get_check_list(self):
            print(check)
