from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.test.v2.test_data import ltc_test_address
from blockapi.v2.api.bitaps import BitapsLitecoinApi
from blockapi.v2.models import FetchResult


def test_fetch_balances(requests_mock, bitaps_ltc_balance_response):
    requests_mock.get(
        f'https://api.bitaps.com/ltc/v1/blockchain/address/state/{ltc_test_address}',
        text=bitaps_ltc_balance_response,
    )

    api = BitapsLitecoinApi()
    balances = api.get_balance(ltc_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('0.00075763')


def test_parse_zero_balance():
    api = BitapsLitecoinApi()
    fetch_result = FetchResult(data={'data': {'balance': 0}})
    result = api.parse_balances(fetch_result)
    assert result.data is None


def test_parse_empty_response():
    api = BitapsLitecoinApi()
    fetch_result = FetchResult(data=None)
    result = api.parse_balances(fetch_result)
    assert result.data is None


@pytest.fixture
def bitaps_ltc_balance_response():
    return read_file('data/bitaps_ltc_balance_response.json')
