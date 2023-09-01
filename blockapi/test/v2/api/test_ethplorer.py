from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api import EthplorerApi

eth_test_address = '0x539C92186f7C6CC4CbF443F26eF84C595baBBcA1'


@pytest.fixture
def eth_balance_response():
    return read_file('data/ethplorer_balance_response.json')


def test_get_balances(requests_mock, eth_balance_response):
    requests_mock.get(
        f'https://api.ethplorer.io/getAddressInfo/{eth_test_address}?apiKey=freekey',
        text=eth_balance_response,
    )

    api = EthplorerApi()
    balances = api.get_balance(eth_test_address)
    assert len(balances) == 38
    assert balances[0].balance == Decimal('250000.000036')
