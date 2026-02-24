from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.test.v2.test_data import zec_test_address
from blockapi.v2.api import BlockchairZcashApi


def test_fetch_balances(requests_mock, zec_balance_response):
    requests_mock.get(
        f'https://api.blockchair.com/zcash/dashboards/address/{zec_test_address}?limit=10,0&offset=0,0',
        text=zec_balance_response,
    )

    api = BlockchairZcashApi()
    balances = api.get_balance(zec_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('0')


def test_fetch_transactions(
    requests_mock, zec_balance_response, zec_transactions_response
):
    requests_mock.get(
        f'https://api.blockchair.com/zcash/dashboards/address/{zec_test_address}?limit=1,0&offset=0,0',
        text=zec_balance_response,
    )

    # noinspection SpellCheckingInspection
    transactions = [
        '6a8e7c951e76c6c5978125d66681798918a52140d1fe59bf67a5a971898e2972',
    ]

    requests_mock.get(
        'https://api.blockchair.com/zcash/dashboards/transactions/'
        + ','.join(transactions),
        text=zec_transactions_response,
    )

    api = BlockchairZcashApi()

    txs = api.get_transactions(zec_test_address, limit=1)
    assert len(txs) == 1
    assert txs[0].operations[0].amount == Decimal('247988.586838')


@pytest.fixture()
def zec_transactions_response():
    return read_file('data/blockchair_zec_transaction_response.json')


@pytest.fixture
def zec_balance_response():
    return read_file('data/blockchair_zec_balance_response.json')
