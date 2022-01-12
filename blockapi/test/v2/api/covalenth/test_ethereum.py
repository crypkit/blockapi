import json
import os.path

# TODO: add requirements!
import pytest

from blockapi.v2.api.covalenth.ethereum import EthCovalentApi


@pytest.fixture
def covalenth_eth_balances_response():
    json_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "ethereum.json")
    )
    with open(json_path) as f:
        return json.load(f)


@pytest.fixture
def eth_covalent_api():
    return EthCovalentApi(api_key="test_key")


def test_parse_balance(eth_covalent_api, covalenth_eth_balances_response):
    expected_len = len(covalenth_eth_balances_response["data"]["items"])
    parsed_items = list(eth_covalent_api._parse_items(covalenth_eth_balances_response))
    assert len(parsed_items) == expected_len
