from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api.covalenth.bitcoin import BitcoinCovalentApi
from blockapi.v2.models import CoingeckoId


@pytest.fixture
def covalent_btc_balances_response():
    return read_file('data/covalent/bitcoin.json')


@pytest.fixture
def eth_covalent_api():
    return BitcoinCovalentApi(api_key="test_key")


def test_parse_balance(eth_covalent_api, covalent_btc_balances_response, requests_mock):
    requests_mock.get(
        'https://api.covalenthq.com/v1/btc-mainnet/address/some-address/balances_v2/',
        text=covalent_btc_balances_response,
    )
    balances = eth_covalent_api.get_balance('some-address')
    assert len(balances) == 1
    assert balances[0].balance == Decimal('109.07')
    assert balances[0].coin.info.coingecko_id == CoingeckoId.BITCOIN
