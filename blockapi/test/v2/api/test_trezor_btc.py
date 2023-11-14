from decimal import Decimal

import pytest
from urllib3.exceptions import ProtocolError

from blockapi.test.v2.api.conftest import read_file
from blockapi.test.v2.test_data import btc_test_address, xpub_test_address
from blockapi.v2.api import TrezorBitcoin1Api, TrezorBitcoin2Api
from blockapi.v2.base import ApiException
from blockapi.v2.models import FetchResult


def test_fetch_balances_1(requests_mock, trezor_btc_1_balance_response):
    requests_mock.get(
        f'https://btc1.trezor.io/api/v2/address/{btc_test_address}',
        text=trezor_btc_1_balance_response,
    )

    api = TrezorBitcoin1Api()
    balances = api.get_balance(btc_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('0.00064363')


def test_fetch_only(requests_mock, trezor_btc_1_balance_response):
    requests_mock.get(
        f'https://btc1.trezor.io/api/v2/address/{btc_test_address}',
        text=trezor_btc_1_balance_response,
    )

    api = TrezorBitcoin1Api()
    result = api.fetch_balances(btc_test_address)
    assert result.data['balance'] == '64363'


def test_fetch_raises_exception(requests_mock):
    requests_mock.get(
        f'https://btc1.trezor.io/api/v2/address/{btc_test_address}',
        exc=ProtocolError('Source disconnected error'),
    )

    api = TrezorBitcoin1Api()
    result = api.fetch_balances(btc_test_address)
    assert result.errors == ['ProtocolError: Source disconnected error']
    assert not result.data


def test_fetch_error_response(requests_mock):
    requests_mock.get(
        f'https://btc1.trezor.io/api/v2/address/{btc_test_address}',
        status_code=503,
        reason='Error description',
    )

    api = TrezorBitcoin1Api()
    result = api.fetch_balances(btc_test_address)
    assert result.errors == ['Error description']


def test_get_balance_should_rise(requests_mock):
    requests_mock.get(
        f'https://btc1.trezor.io/api/v2/address/{btc_test_address}',
        status_code=503,
        reason='Error description',
    )

    api = TrezorBitcoin1Api()
    with pytest.raises(ApiException, match='Error description'):
        result = api.get_balance(btc_test_address)


def test_parse_only():
    api = TrezorBitcoin1Api()
    fetch_result = FetchResult(data=dict(balance='64363'))
    result = api.parse_balances(fetch_result)
    assert result.data[0].balance == Decimal('0.00064363')


def test_fetch_balances_2(requests_mock, trezor_btc_2_balance_response):
    requests_mock.get(
        f'https://btc2.trezor.io/api/v2/address/{btc_test_address}',
        text=trezor_btc_2_balance_response,
    )

    api = TrezorBitcoin2Api()
    balances = api.get_balance(btc_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('0.00064363')


def test_fetch_balances_xpub_1(requests_mock, trezor_xpub_1_balance_response):
    requests_mock.get(
        f'https://btc1.trezor.io/api/v2/xpub/{xpub_test_address}',
        text=trezor_xpub_1_balance_response,
    )

    api = TrezorBitcoin1Api()
    balances = api.get_balance(xpub_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('0.12706308')


def test_fetch_balances_xpub_2(requests_mock, trezor_xpub_2_balance_response):
    requests_mock.get(
        f'https://btc2.trezor.io/api/v2/xpub/{xpub_test_address}',
        text=trezor_xpub_2_balance_response,
    )

    api = TrezorBitcoin2Api()
    balances = api.get_balance(xpub_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('0.12706308')


@pytest.fixture
def trezor_btc_1_balance_response():
    return read_file('data/trezor_btc_1_balance_response.json')


@pytest.fixture
def trezor_btc_2_balance_response():
    return read_file('data/trezor_btc_2_balance_response.json')


@pytest.fixture
def trezor_xpub_1_balance_response():
    return read_file('data/trezor_xpub_1_balance_response.json')


@pytest.fixture
def trezor_xpub_2_balance_response():
    return read_file('data/trezor_xpub_2_balance_response.json')
