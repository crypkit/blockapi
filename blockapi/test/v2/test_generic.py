import pytest

from blockapi.test.v2.test_data import (
    BAD_ADDRESSES,
    DEBANK_API_KEY,
    NON_EMPTY_VALID_ADDRESSES_BY_SYMBOL,
    get_debank_addresses,
    yield_all_api_classes,
    yield_api_instances,
)
from blockapi.v2.api import DebankApi, OptimismEtherscanApi
from blockapi.v2.base import ApiException
from blockapi.v2.models import AssetType, BalanceItem, Blockchain


@pytest.mark.integration
@pytest.mark.parametrize('api_instance', yield_api_instances())
def test_get_balance_for_valid_non_empty_address(api_instance):
    for address in NON_EMPTY_VALID_ADDRESSES_BY_SYMBOL.get(
        api_instance.coin.symbol, []
    ):
        balances = api_instance.get_balance(address)

        assert all(isinstance(b, BalanceItem) for b in balances)
        assert len(balances) > 0


@pytest.mark.integration
@pytest.mark.parametrize('api_instance', yield_api_instances())
def test_get_balance_for_bad_address(api_instance):
    if isinstance(api_instance, OptimismEtherscanApi):
        # OptimismEtherscanApi does not validate addresses, so we skip it.
        return

    for address in BAD_ADDRESSES:
        with pytest.raises(ApiException):
            api_instance.get_balance(address)


@pytest.mark.integration
@pytest.mark.parametrize('address', get_debank_addresses())
def test_get_balance_for_debank(address):
    api_instance = DebankApi(DEBANK_API_KEY, False)
    balances = api_instance.get_balance(address)

    assert all(isinstance(b, BalanceItem) for b in balances)
    assert all(AssetType(b.asset_type) is not None for b in balances)
    assert all(Blockchain(b.coin.blockchain) is not None for b in balances)
    assert len(balances) > 0


@pytest.mark.integration
@pytest.mark.parametrize('address', get_debank_addresses())
def test_get_portfolio_for_debank(address):
    api_instance = DebankApi(DEBANK_API_KEY, False)
    pools = api_instance.get_portfolio(address)

    balances = [item for pool in pools for item in pool.items]

    assert all(isinstance(b, BalanceItem) for b in balances)
    assert all(AssetType(b.asset_type) is not None for b in balances)
    assert all(Blockchain(b.coin.blockchain) is not None for b in balances)
    assert len(balances) > 0


@pytest.mark.parametrize('api_instance', yield_all_api_classes())
def test_verify_repr_for_instance(api_instance):
    assert repr(api_instance)
