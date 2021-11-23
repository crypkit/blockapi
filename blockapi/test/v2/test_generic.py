import pytest

from httpx import HTTPError

from blockapi.test.v2.test_data import (
    yield_api_instances_for_non_empty_valid_addresses,
    yield_api_instances_for_bad_addresses,
)
from blockapi.v2.models import BalanceItem


@pytest.mark.parametrize(
    'api_instance', yield_api_instances_for_non_empty_valid_addresses()
)
def test_get_balance_for_valid_non_empty_address(api_instance):
    balances = api_instance.get_balance()

    assert all(isinstance(b, BalanceItem) for b in balances)
    assert len(balances) > 0


@pytest.mark.parametrize(
    'api_instance', yield_api_instances_for_bad_addresses()
)
def test_get_balance_for_bad_address(api_instance):
    with pytest.raises(HTTPError):
        api_instance.get_balance()
