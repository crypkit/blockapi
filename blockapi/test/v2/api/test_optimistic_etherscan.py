from decimal import Decimal

import pytest

from blockapi.v2.api.optimistic_etherscan import OptimismEtherscanApi

ETH_BALANCE = '248936789990053052'


@pytest.fixture
def optimism_etherscan_api():
    return OptimismEtherscanApi(api_key="test_key")


@pytest.fixture
def api_response():
    return {'status': '1', 'message': 'OK', 'result': ETH_BALANCE}


def test_parse_eth_balance(optimism_etherscan_api, api_response):
    parsed_balance = optimism_etherscan_api._parse_eth_balance(api_response)
    assert parsed_balance.balance_raw == Decimal(ETH_BALANCE)
    assert parsed_balance.raw == api_response
