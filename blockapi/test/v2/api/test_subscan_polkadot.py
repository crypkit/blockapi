from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api.subscan import PolkadotSubscanApi


@pytest.mark.parametrize(
    'address, response_path, expected_balance',
    [
        (
            '1NjjK81oA9is7eWhFJ7n7kQhaPT3pnxLFH5MkwDfduAiWE9',
            'data/subscan_polkadot_response_WE9.json',
            Decimal('4649.9139999889'),
        ),
        (
            '15j4dg5GzsL1bw2U2AWgeyAk6QTxq43V7ZPbXdAmbVLjvDCK',
            'data/subscan_polkadot_response_DCK.json',
            Decimal('49296244.7887007465'),
        ),
    ],
)
def test_fetch_balances(requests_mock, address, response_path, expected_balance):
    requests_mock.post(
        'https://polkadot.api.subscan.io/api/v2/scan/search',
        text=read_file(response_path),
    )

    api = PolkadotSubscanApi()
    balances = api.get_balance(address)
    assert sum(b.balance for b in balances) == expected_balance
