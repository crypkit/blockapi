from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.test.v2.test_data import ltc_test_address
from blockapi.v2.api.litecoinspace import LitecoinSpaceApi
from blockapi.v2.models import FetchResult


def test_fetch_balances(requests_mock, litecoinspace_balance_response):
    requests_mock.get(
        f'https://litecoinspace.org/api/address/{ltc_test_address}',
        text=litecoinspace_balance_response,
    )

    api = LitecoinSpaceApi()
    balances = api.get_balance(ltc_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('0.00075763')


def test_parse_zero_balance():
    api = LitecoinSpaceApi()
    fetch_result = FetchResult(
        data={
            'chain_stats': {
                'funded_txo_sum': 100,
                'spent_txo_sum': 100,
            }
        }
    )
    result = api.parse_balances(fetch_result)
    assert result.data is None


def test_parse_empty_response():
    api = LitecoinSpaceApi()
    fetch_result = FetchResult(data=None)
    result = api.parse_balances(fetch_result)
    assert result.data is None


@pytest.fixture
def litecoinspace_balance_response():
    return read_file('data/litecoinspace_balance_response.json')
