import pytest
import monitoring.checker
import monitoring.settings


def test_checker_run(mocker):
    # Creating Checker object
    sender = mocker.Mock()
    checker = monitoring.checker.Checker(sender=sender)
    sender.assert_called_once_with()

    # Mocking every calls and execute checker.run()
    mocker.patch("monitoring.checker.Checker.get_check_list", return_value=["dummy"])
    mocker.patch("monitoring.checker.Checker.perform_check", return_value="dummy2")
    checker.run()

    # Checking that mocks are still actual
    monitoring.checker.Checker.get_check_list.assert_called_once_with()
    monitoring.checker.Checker.perform_check.assert_called_once_with("dummy")
    checker.sender.send.assert_called_once_with("dummy2")


def test_checker_get_check_list(mocker):
    checker = monitoring.checker.Checker(sender=mocker.Mock())

    monitoring.settings.cfg["checks"] = [{"url": "test-url"}]
    check_list = checker.get_check_list()
    assert check_list[0]["url"] == "test-url"

