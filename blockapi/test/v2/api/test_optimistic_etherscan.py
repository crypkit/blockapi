from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api import OptimismEtherscanApi

ETH_BALANCE = '248936789990053052'

eth_test_address = '0x539C92186f7C6CC4CbF443F26eF84C595baBBcA1'


@pytest.fixture
def optimism_etherscan_api():
    return OptimismEtherscanApi(api_key="test_key")


@pytest.fixture
def api_response():
    return {'status': '1', 'message': 'OK', 'result': ETH_BALANCE}


@pytest.fixture
def eth_balance_response():
    return read_file('data/optimistic_etherscan_balance_response.json')


def test_parse_eth_balance(optimism_etherscan_api, api_response):
    parsed_balance = optimism_etherscan_api._parse_eth_balance(api_response)
    assert parsed_balance.balance_raw == Decimal(ETH_BALANCE)
    assert parsed_balance.raw == api_response


def test_get_balances(optimism_etherscan_api, requests_mock, eth_balance_response):
    requests_mock.get(
        f'https://api-optimistic.etherscan.io/api?module=account&action=balance&address={eth_test_address}&tag=latest&apikey=test_key',
        text=eth_balance_response,
    )

    balances = optimism_etherscan_api.get_balance(eth_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('1')
