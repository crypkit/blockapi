from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.test.v2.test_data import zec_test_address
from blockapi.v2.api import TrezorZcashApi
from blockapi.v2.base import ApiException
from blockapi.v2.models import FetchResult


def test_fetch_balances(requests_mock, trezor_zec_balance_response):
    requests_mock.get(
        f'https://blockbook.zec.zelcore.io/api/v2/address/{zec_test_address}',
        text=trezor_zec_balance_response,
    )

    api = TrezorZcashApi()
    balances = api.get_balance(zec_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('12.345')


def test_fetch_only(requests_mock, trezor_zec_balance_response):
    requests_mock.get(
        f'https://blockbook.zec.zelcore.io/api/v2/address/{zec_test_address}',
        text=trezor_zec_balance_response,
    )

    api = TrezorZcashApi()
    result = api.fetch_balances(zec_test_address)
    assert result.data['balance'] == '1234500000'


def test_parse_only():
    api = TrezorZcashApi()
    fetch_result = FetchResult(data=dict(balance='1234500000'))
    result = api.parse_balances(fetch_result)
    assert result.data[0].balance == Decimal('12.345')


def test_parse_zero_balance():
    api = TrezorZcashApi()
    fetch_result = FetchResult(data=dict(balance='0'))
    result = api.parse_balances(fetch_result)
    assert result.data is None


def test_fetch_invalid_address(requests_mock):
    invalid_address = 'not-a-valid-zec-address'
    requests_mock.get(
        f'https://blockbook.zec.zelcore.io/api/v2/address/{invalid_address}',
        status_code=400,
        reason='Bad Request',
    )

    api = TrezorZcashApi()
    result = api.fetch_balances(invalid_address)
    assert result.errors == ['Bad Request']


def test_get_balance_invalid_address_should_raise(requests_mock):
    invalid_address = 'not-a-valid-zec-address'
    requests_mock.get(
        f'https://blockbook.zec.zelcore.io/api/v2/address/{invalid_address}',
        status_code=400,
        reason='Bad Request',
    )

    api = TrezorZcashApi()
    with pytest.raises(ApiException, match='Bad Request'):
        api.get_balance(invalid_address)


def test_fetch_error_response(requests_mock):
    requests_mock.get(
        f'https://blockbook.zec.zelcore.io/api/v2/address/{zec_test_address}',
        status_code=500,
        reason='Internal Server Error',
    )

    api = TrezorZcashApi()
    result = api.fetch_balances(zec_test_address)
    assert result.errors == ['Internal Server Error']


def test_get_balance_should_raise(requests_mock):
    requests_mock.get(
        f'https://blockbook.zec.zelcore.io/api/v2/address/{zec_test_address}',
        status_code=500,
        reason='Internal Server Error',
    )

    api = TrezorZcashApi()
    with pytest.raises(ApiException, match='Internal Server Error'):
        api.get_balance(zec_test_address)


@pytest.fixture
def trezor_zec_balance_response():
    return read_file('data/trezor_zec_balance_response.json')
