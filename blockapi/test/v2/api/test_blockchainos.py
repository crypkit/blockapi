from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api.blockchainos import BlockchainosApi

# noinspection SpellCheckingInspection
test_address = 'GCPQQIX2LRX2J63C7AHWDXEMNGMZR2UI2PRN5TCSOVMEMF7BAUADMKH5'


@pytest.fixture
def api():
    return BlockchainosApi()


def test_fetch_balances(requests_mock, api, bos_balance_response):
    requests_mock.get(
        f'https://mainnet.blockchainos.org/api/v1/accounts/{test_address}',
        text=bos_balance_response,
    )

    balances = api.get_balance(test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('1012356993.757')
    assert balances[0].balance == balances[0].balance_raw * Decimal('1e-7')


def test_fetch_transactions(
    requests_mock, api, bos_transactions_response, bos_operations_responses
):
    create_transaction_mocks(
        bos_operations_responses, bos_transactions_response, requests_mock
    )

    txs = api.get_transactions(test_address, limit=3)
    assert len(txs) == 3
    assert txs[0].fee == Decimal('0')
    assert len(txs[0].operations) == 2
    assert txs[0].operations[1].amount == Decimal('50')


def create_transaction_mocks(
    bos_operations_responses, bos_transactions_response, requests_mock
):
    requests_mock.get(
        f'https://mainnet.blockchainos.org/api/v1/accounts/{test_address}/transactions?limit=3&reverse=true',
        text=bos_transactions_response,
    )
    for hash, responses in bos_operations_responses.items():
        for index in range(len(responses)):
            requests_mock.get(
                f'https://mainnet.blockchainos.org/api/v1/transactions/{hash}/operations/{index}',
                text=responses[index],
            )


@pytest.fixture()
def bos_transactions_response():
    return read_file('data/bos_transaction_response.json')


@pytest.fixture
def bos_balance_response():
    return read_file('data/bos_balance_response.json')


@pytest.fixture()
def bos_operations_responses():
    # noinspection SpellCheckingInspection
    return {
        '8tok9mHjGURhcnbLkrhcEDgQoXvoYjLVs2ipxAAsi2d6': [
            read_file('data/bos_operations_response_8t_1.json'),
            read_file('data/bos_operations_response_8t_2.json'),
        ],
        "R1nddzPKA5uh5a7ZTjS113aUth9t1Bv68hjjjxGCqgS": [
            read_file('data/bos_operations_response_r1_1.json'),
            read_file('data/bos_operations_response_r1_2.json'),
        ],
    }
