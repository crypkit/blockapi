import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api.covalenth.ethereum import EthCovalentApi


@pytest.fixture
def covalent_eth_balances_response():
    return read_file('data/covalent/ethereum.json')


@pytest.fixture
def eth_covalent_api():
    return EthCovalentApi(api_key="test_key")


def test_parse_balance(eth_covalent_api, covalent_eth_balances_response, requests_mock):
    requests_mock.get(
        'https://api.covalenthq.com/v1/1/address/0x1234/balances_v2/',
        text=covalent_eth_balances_response,
    )
    balances = eth_covalent_api.get_balance('0x1234')
    assert len(balances) == 121
