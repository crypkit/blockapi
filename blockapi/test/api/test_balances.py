from typing import Type

from blockapi import get_active_api_classes
from blockapi.services import BlockchainAPI
from blockapi.test_data import get_test_api_key, test_addresses


# TODO parametrize it for all endpoints using pytest
def _test_balances():
    for api_cls in get_active_api_classes():
        addr = test_addresses[api_cls.symbol][0]
        try:
            assert_balance(api_cls, addr)
        except AssertionError as e:
            print(e)


def assert_balance(api_cls: Type[BlockchainAPI], address: str):
    api_key = get_test_api_key(api_cls.__class__.__name__)
    api_inst = api_cls(address, api_key)

    balances = api_inst.get_balance()
    check_balance = next((b for b in balances if b['symbol'] == api_inst.symbol), None)

    assert check_balance, (
        f"No balance for symbol {api_inst.symbol} and API "
        f"{api_cls.__class__.__name__}."
    )
