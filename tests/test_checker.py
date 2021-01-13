import pytest
import monitoring.checker
import monitoring.settings
from monitoring.check_models import CheckParams
from unittest.mock import MagicMock
import redis


def test_checker_run(mocker):
    # Creating Checker object (with mocked Kafka and Redis)
    sender = mocker.Mock()
    mocker.patch("redis.Redis")

    checker = monitoring.checker.Checker(sender=sender)
    sender.assert_called_once_with()

    # Mocking every call and execute checker.run()
    checker.redis = mocker.Mock()
    attrs = {
        "get.return_value": None,
        "set.return_value": None,
    }
    checker.redis.configure_mock(**attrs)
    check_param = CheckParams(url="dummy")
    mocker.patch(
        "monitoring.checker.Checker.get_check_list", return_value=[check_param]
    )
    mocker.patch("monitoring.checker.Checker.perform_check", return_value="dummy2")
    checker.run()

    # Checking that mocks are still actual
    checker.redis.get.assert_called_once_with(check_param.url)
    checker.redis.set.assert_called_once_with("dummy", 1, ex=60)
    monitoring.checker.Checker.get_check_list.assert_called_once_with()
    monitoring.checker.Checker.perform_check.assert_called_once_with(check_param)
    checker.sender.send.assert_called_once_with("dummy2")


def test_checker_get_check_list(mocker):
    checker = monitoring.checker.Checker(sender=mocker.Mock())

    monitoring.settings.cfg["checks"] = [{"url": "test-url"}]
    check_list = checker.get_check_list()
    assert check_list[0].url == "test-url"


def test_checker_perform_check_200_ok(mocker):
    """ Treating 200 as success """
    checker = monitoring.checker.Checker(sender=mocker.Mock())
    get_result = MagicMock()

    check_param = CheckParams(
        url="my-url",
    )
    get_result.status_code = 200

    mocker.patch("requests.get", return_value=get_result)
    check_list = checker.perform_check(check_param)
    assert check_list.success == True
    assert check_list.url == check_param.url
    assert check_list.expected_code == 200
    assert check_list.regexp == ""


def test_checker_perform_check_502_fail(mocker):
    """ Treating 200 as success """
    checker = monitoring.checker.Checker(sender=mocker.Mock())
    get_result = MagicMock()

    check_param = CheckParams(
        url="my-url",
    )
    get_result.status_code = 502

    mocker.patch("requests.get", return_value=get_result)
    check_list = checker.perform_check(check_param)
    assert check_list.success == False


def test_checker_perform_check_200_fail(mocker):
    """ Treating 200 as fail because of different expected_code """
    checker = monitoring.checker.Checker(sender=mocker.Mock())
    get_result = MagicMock()

    check_param = CheckParams(
        url="my-url",
        expected_code=302,
    )
    get_result.status_code = 200

    mocker.patch("requests.get", return_value=get_result)
    check_list = checker.perform_check(check_param)
    assert check_list.success == False


def test_checker_perform_check_regexp_ok(mocker):
    """ Treating 200 as fail because of different expected_code """
    checker = monitoring.checker.Checker(sender=mocker.Mock())
    get_result = MagicMock()

    check_param = CheckParams(
        url="my-url",
        regexp="J.ck",
    )
    get_result.status_code = 200
    get_result.content = "All work and no play makes Jack a dull boy"

    mocker.patch("requests.get", return_value=get_result)
    check_list = checker.perform_check(check_param)
    assert check_list.success == True
    assert check_list.regexp == check_param.regexp
    assert check_list.response_length == len(get_result.content)


def test_checker_perform_check_regexp_ok(mocker):
    """ Treating 200 as fail because of different expected_code """
    checker = monitoring.checker.Checker(sender=mocker.Mock())
    get_result = MagicMock()

    check_param = CheckParams(
        url="my-url",
        regexp="J.ck",
    )
    get_result.status_code = 200
    get_result.content = "All work and no play makes James a dull boy"

    mocker.patch("requests.get", return_value=get_result)
    check_list = checker.perform_check(check_param)
    assert check_list.success == False
    assert check_list.regexp == check_param.regexp
    assert check_list.response_length == len(get_result.content)