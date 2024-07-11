from unittest.mock import MagicMock, patch

import pytest
from requests import HTTPError
from requests.exceptions import ConnectionError as RequestsConnectionError

from blockapi.v2.base import CustomizableBlockchainApi
from build.lib.blockapi.test.v2.api.fake_sleep_provider import FakeSleepProvider


@pytest.fixture()
def customizable_api():
    yield CustomizableBlockchainApi("fake_base", sleep_provider=FakeSleepProvider())


@pytest.fixture()
def mocked_get_response_with_some_errors():
    mocked_response = MagicMock()
    mocked_response.status_code = 200
    mocked_response.json.return_value = {}
    mocked_response.headers = {}

    with patch('blockapi.v2.base.CustomizableBlockchainApi._get_response') as patched:
        patched.side_effect = [
            RequestsConnectionError("Wrong!"),
            RequestsConnectionError("Wrong!"),
            mocked_response,
        ]
        yield patched


def test_get_data_connection_error_success(
    customizable_api, mocked_get_response_with_some_errors
):
    response = customizable_api.get_data("test_method")

    assert response.status_code == 200


@pytest.fixture()
def mocked_get_response_with_only_errors():
    with patch('blockapi.v2.base.CustomizableBlockchainApi._get_response') as patched:
        patched.side_effect = [
            RequestsConnectionError("Wrong!"),
            RequestsConnectionError("Wrong!"),
            RequestsConnectionError("Wrong!"),
            RequestsConnectionError("Wrong!"),
            RequestsConnectionError("Wrong!"),
        ]
        yield patched


def test_get_data_connection_error(
    customizable_api, mocked_get_response_with_only_errors
):
    response = customizable_api.get_data("test_method")
    assert response.status_code == 1


@pytest.fixture()
def mocked_get_response_with_exception():
    with patch('blockapi.v2.base.CustomizableBlockchainApi._get_response') as patched:
        patched.side_effect = Exception("Stoppie!")
        yield patched


def test_get_data_exception(customizable_api, mocked_get_response_with_exception):
    response = customizable_api.get_data("test_method")
    assert response.status_code == 2


@pytest.fixture()
def mocked_unauthorized_response():
    mocked_response = MagicMock()
    mocked_response.status_code = 401
    mocked_response.raise_for_status.side_effect = HTTPError(
        "test_method", 401, "exception", {}, None
    )
    mocked_response.json.return_value = {}
    mocked_response.headers = {}

    with patch('blockapi.v2.base.CustomizableBlockchainApi._get_response') as patched:
        patched.side_effect = [
            mocked_response,
        ]
        yield patched


def test_unauthorized_will_not_retry(customizable_api, mocked_unauthorized_response):
    response = customizable_api.get_data("test_method")
    assert response.status_code == 401


@pytest.fixture()
def mocked_500_with_success_response():
    mocked_failure = MagicMock()
    mocked_failure.status_code = 500
    mocked_failure.raise_for_status.side_effect = HTTPError(
        "test_method", 500, "exception", {}, None
    )
    mocked_failure.json.return_value = {}
    mocked_failure.headers = {}

    mocked_success = MagicMock()
    mocked_success.status_code = 200
    mocked_success.json.return_value = {}
    mocked_success.headers = {}

    with patch('blockapi.v2.base.CustomizableBlockchainApi._get_response') as patched:
        patched.side_effect = [
            mocked_failure,
            mocked_success,
        ]
        yield patched


def test_5xx_will_retry(customizable_api, mocked_500_with_success_response):
    response = customizable_api.get_data("test_method")
    assert response.status_code == 200
