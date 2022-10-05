from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api.blockchair import BlockchairLitecoinApi

# noinspection SpellCheckingInspection
ltc_test_address = 'M8T1B2Z97gVdvmfkQcAtYbEepune1tzGua'


def test_fetch_balances(requests_mock, ltc_balance_response):
    requests_mock.get(
        f'https://api.blockchair.com/litecoin/dashboards/address/{ltc_test_address}?limit=10,0&offset=0,0',
        text=ltc_balance_response,
    )

    api = BlockchairLitecoinApi()
    balances = api.get_balance(ltc_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('2524667.31490873')


def test_fetch_transactions(
    requests_mock, ltc_balance_response, ltc_transactions_response
):
    requests_mock.get(
        f'https://api.blockchair.com/litecoin/dashboards/address/{ltc_test_address}?limit=3,0&offset=0,0',
        text=ltc_balance_response,
    )

    # noinspection SpellCheckingInspection
    addresses = [
        "6b6065edce69d513d81bd2960562062577e1678ee07a24f54d2c5bb660b8ab22",
    ]

    requests_mock.get(
        'https://api.blockchair.com/litecoin/dashboards/transactions/'
        + ','.join(addresses),
        text=ltc_transactions_response,
    )

    api = BlockchairLitecoinApi()

    txs = api.get_transactions(ltc_test_address, limit=3)
    assert len(txs) == 1
    assert txs[0].fee == Decimal('0')
    assert len(txs[0].operations) == 1
    assert txs[0].operations[0].amount == Decimal('0.0002')


@pytest.fixture()
def ltc_transactions_response():
    return read_file('data/blockchair_ltc_transaction_response.json')


@pytest.fixture
def ltc_balance_response():
    return read_file('data/blockchair_ltc_balance_response.json')
