from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.test.v2.test_data import btc_test_address
from blockapi.v2.api import BlockchairBitcoinApi


def test_fetch_balances(requests_mock, btc_balance_response):
    requests_mock.get(
        f'https://api.blockchair.com/bitcoin/dashboards/address/{btc_test_address}?limit=10,0&offset=0,0',
        text=btc_balance_response,
    )

    api = BlockchairBitcoinApi()
    balances = api.get_balance(btc_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('0.00064363')


def test_fetch_transactions(
    requests_mock, btc_balance_response, btc_transactions_response
):
    requests_mock.get(
        f'https://api.blockchair.com/bitcoin/dashboards/address/{btc_test_address}?limit=3,0&offset=0,0',
        text=btc_balance_response,
    )

    # noinspection SpellCheckingInspection
    transactions = [
        "3fcb8ac40fd7e1bfe2a95b6704d8af3bbd88640c0177ec118e26e06d3a06cc07",
        "e39457afee2730fa3eac9016efa02dac1c28998b60e87efdaa604ed0d175567f",
        "21cc75fd255111ebc9a4c81ce08c45f26e8d8721b4a8912452648ca9ff9d54c1",
    ]

    requests_mock.get(
        'https://api.blockchair.com/bitcoin/dashboards/transactions/'
        + ','.join(transactions),
        text=btc_transactions_response,
    )

    api = BlockchairBitcoinApi()

    txs = api.get_transactions(btc_test_address, limit=3)
    assert len(txs) == 1
    assert txs[0].fee == Decimal('0.00056963')
    assert len(txs[0].operations) == 1
    assert txs[0].operations[0].amount == Decimal('0.20087268')


@pytest.fixture()
def btc_transactions_response():
    return read_file('data/blockchair_btc_transaction_response.json')


@pytest.fixture
def btc_balance_response():
    return read_file('data/blockchair_btc_balance_response.json')
