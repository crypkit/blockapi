import pytest

from blockapi.test.v2.test_data import (
    BAD_ADDRESSES,
    NON_EMPTY_VALID_ADDRESSES_BY_SYMBOL,
    yield_api_instances,
)
from blockapi.v2.api.optimistic_etherscan import OptimismEtherscanApi
from blockapi.v2.base import ApiException
from blockapi.v2.models import BalanceItem


@pytest.mark.parametrize('api_instance', yield_api_instances())
def test_get_balance_for_valid_non_empty_address(api_instance):
    for address in NON_EMPTY_VALID_ADDRESSES_BY_SYMBOL.get(
        api_instance.coin.symbol, []
    ):
        balances = api_instance.get_balance(address)

        assert all(isinstance(b, BalanceItem) for b in balances)
        assert len(balances) > 0


@pytest.mark.parametrize('api_instance', yield_api_instances())
def test_get_balance_for_bad_address(api_instance):
    if isinstance(api_instance, OptimismEtherscanApi):
        # OptimismEtherscanApi does not validate addresses, so we skip it.
        return

    for address in BAD_ADDRESSES:
        with pytest.raises(ApiException):
            api_instance.get_balance(address)
