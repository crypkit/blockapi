from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file

# noinspection SpellCheckingInspection
btc_test_address = '35hK24tcLEWcgNA4JxpvbkNkoAcDGqQPsP'
# noinspection SpellCheckingInspection
xpub_test_address = 'xpub6CUGRUonZSQ4TWtTMmzXdrXDtypWKiKrhko4egpiMZbpiaQL2jkwSB1icqYh2cfDfVxdx4df189oLKnC5fSwqPfgyP3hooxujYzAu3fDVmz'
from blockapi.v2.api import BlockchainInfoApi
from blockapi.v2.base import ApiException
from blockapi.v2.models import FetchResult


def test_fetch_balances(requests_mock, blockchain_info_balance_response):
    requests_mock.get(
        'https://blockchain.info/multiaddr',
        text=blockchain_info_balance_response,
    )

    api = BlockchainInfoApi()
    balances = api.get_balance(btc_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('0.00064363')


def test_fetch_balances_xpub(requests_mock, blockchain_info_xpub_response):
    requests_mock.get(
        'https://blockchain.info/multiaddr',
        text=blockchain_info_xpub_response,
    )

    api = BlockchainInfoApi()
    balances = api.get_balance(xpub_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('0.12706308')


def test_fetch_only(requests_mock, blockchain_info_balance_response):
    requests_mock.get(
        'https://blockchain.info/multiaddr',
        text=blockchain_info_balance_response,
    )

    api = BlockchainInfoApi()
    result = api.fetch_balances(btc_test_address)
    assert result.data['wallet']['final_balance'] == 64363


def test_parse_only():
    api = BlockchainInfoApi()
    fetch_result = FetchResult(data={'wallet': {'final_balance': 64363}})
    result = api.parse_balances(fetch_result)
    assert result.data[0].balance == Decimal('0.00064363')


def test_fetch_error_response(requests_mock):
    requests_mock.get(
        'https://blockchain.info/multiaddr',
        status_code=500,
        reason='Internal Server Error',
    )

    api = BlockchainInfoApi()
    result = api.fetch_balances(btc_test_address)
    assert result.errors == ['Internal Server Error']


def test_get_balance_should_raise(requests_mock):
    requests_mock.get(
        'https://blockchain.info/multiaddr',
        status_code=500,
        reason='Internal Server Error',
    )

    api = BlockchainInfoApi()
    with pytest.raises(ApiException, match='Internal Server Error'):
        api.get_balance(btc_test_address)


@pytest.fixture
def blockchain_info_balance_response():
    return read_file('data/blockchain_info_balance_response.json')


@pytest.fixture
def blockchain_info_xpub_response():
    return read_file('data/blockchain_info_xpub_response.json')
