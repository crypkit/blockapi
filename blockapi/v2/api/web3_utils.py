import functools
import logging
import os
from typing import List, Optional, Tuple, Union

from web3 import Web3
from web3.contract import Contract
from web3.types import BlockIdentifier

_web3_patched = False
LATEST_BLOCK: BlockIdentifier = "latest"

logger = logging.getLogger(__name__)

env_variables = os.environ


def easy_call(
    contract: Contract,
    function_name: str,
    *f_args: Union[bytes, int, str, List[str], Tuple[str]],
    block: Optional[BlockIdentifier] = None,
) -> Union[int, str, dict, List[dict]]:
    """
    Call smart contract function, handle errors and structure results.
    Args:
        contract: web3 smart contract object
        function_name: name of function to call
        f_args: function arguments
        block: block for which function is called

    Returns (int, str, dict or List[dict]):
        Parsed result.
    """
    if not block:
        block = LATEST_BLOCK

    # TODO add errors handling
    f = getattr(contract.functions, function_name)
    try:
        raw = f(*f_args).call(block_identifier=block)
    except Exception as e:
        logging.error(
            "Failed to call function: %s, on contract: %s",
            function_name,
            contract.address,
        )
        raise e

    result = map_struct(raw, contract.abi, function_name)
    return result


def get_eth_client(
    api_url: Optional[str] = None,
) -> Web3:
    """
    Get web3 client.
    Args:
        api_url (string): Full API URL
    """
    return Web3(Web3.HTTPProvider(api_url))


def map_struct(raw_result, abi, func_name):
    """
    Map raw result from smart contract to structured dict (or list
    of dicts).
    Args:
        raw_result (tuple or [tuple]): result from smart contract's call
        abi (dict): ABI definition of whole smart contract
        func_name (str): name of used func

    Returns (dict or [dict]):
        Structured result/s
    """
    func_abi = next(a for a in abi if a.get('name') == func_name)
    components = create_components(func_abi['outputs'])
    component = components[0] if isinstance(components, list) else components

    return (
        [map_sub_item(i, component) for i in raw_result]
        if isinstance(raw_result, list)
        else map_sub_item(raw_result, component)
    )


def map_sub_item(item, component):
    """
    Map component's names to item.
    """
    if not component:
        return item

    sub = {}
    for i, c in zip(item, component.items()):
        key, sub_component = c

        if isinstance(i, list):
            sub[key] = []
            for j in i:
                sub[key].append(map_sub_item(j, sub_component))
        else:
            sub[key] = map_sub_item(i, sub_component)

    return sub


def create_components(abi_outputs):
    """
    Create simple component as nested dict with attributes' names.
    Values of keys are dicts (nested dicts) or None values (if there
    is no more nested item).
    """
    return [create_component(o) for o in abi_outputs]


def create_component(item):
    """
    Create single component from raw_item.
    If there is no nested component, nothing is returned.
    """
    if item.get('components'):
        return {c['name']: create_component(c) for c in item['components']}


def to_checksum_address(func):
    """
    A decorator, which converts input argument representing an Ethereum address
    into its check-summed version. This decorator can be used for class methods
    with address as the first positional argument.
    """

    @functools.wraps(func)
    def inner(self, address, *args, **kwargs):
        return func(self, Web3.toChecksumAddress(address), *args, **kwargs)

    return inner


def ensure_checksum_address(address: Optional[str]) -> Optional[str]:
    return Web3.toChecksumAddress(address) if address is not None else None
