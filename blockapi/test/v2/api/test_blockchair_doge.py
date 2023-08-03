from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api import BlockchairDogecoinApi

# noinspection SpellCheckingInspection
doge_test_address = 'DH5yaieqoZN36fDVciNyRueRGvGLR3mr7L'


def test_fetch_balances(requests_mock, doge_balance_response):
    requests_mock.get(
        f'https://api.blockchair.com/dogecoin/dashboards/address/{doge_test_address}?limit=10,0&offset=0,0',
        text=doge_balance_response,
    )

    api = BlockchairDogecoinApi()
    balances = api.get_balance(doge_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('50285.15921524')


def test_fetch_transactions(
    requests_mock, doge_balance_response, doge_transactions_response
):
    requests_mock.get(
        f'https://api.blockchair.com/dogecoin/dashboards/address/{doge_test_address}?limit=10,0&offset=0,0',
        text=doge_balance_response,
    )

    # noinspection SpellCheckingInspection
    addresses = [
        "ccb2cd37527f725f06ae19f4e46881dc2ac4c5072d9de40a2c563f61536aa7ed",
    ]

    requests_mock.get(
        'https://api.blockchair.com/dogecoin/dashboards/transactions/'
        + ','.join(addresses),
        text=doge_transactions_response,
    )

    api = BlockchairDogecoinApi()

    txs = api.get_transactions(doge_test_address)
    assert len(txs) == 1
    assert txs[0].fee == Decimal('0')
    assert len(txs[0].operations) == 1
    assert txs[0].operations[0].amount == Decimal('31.28571429')


@pytest.fixture()
def doge_transactions_response():
    return read_file('data/blockchair_doge_transaction_response.json')


@pytest.fixture
def doge_balance_response():
    return read_file('data/blockchair_doge_balance_response.json')
