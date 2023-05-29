from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.test.v2.test_data import btc_test_address, xpub_test_address
from blockapi.v2.api.trezor import TrezorBitcoin1Api, TrezorBitcoin2Api


def test_fetch_balances_1(requests_mock, trezor_btc_1_balance_response):
    requests_mock.get(
        f'https://btc1.trezor.io/api/v2/address/{btc_test_address}',
        text=trezor_btc_1_balance_response,
    )

    api = TrezorBitcoin1Api()
    balances = api.get_balance(btc_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('0.00064363')


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
