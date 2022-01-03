import pytest

from blockapi.v2.api.ethplorer import EthplorerApi
from blockapi.v2.api.solana import SolanaApi
from blockapi.v2.api.terra import TerraApi

# TODO create method for auto loading all classes
API_CLASSES = [EthplorerApi, SolanaApi, TerraApi]

NON_EMPTY_VALID_ADDRESSES_BY_SYMBOL = {
    'ETH': [
        '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
    ],
    'SOL': [
        '31dpiondDhZaqK23Re8kzkhY6CFEG9ZTQnr3shQm7g8b',
    ],
    'LUNA': [
        'terra1yltenl48mhl370ldpyt83werd9x3s645509gaf',
    ],
}

BAD_ADDRESSES = [
    '1',
    '10000',
    'AAAAA',
    '0x123',
    'ýžýščš&^^~',
    '0xAF3E9eF83B1dc9Db18cD5923e3112F6Cd8bfDAeX',
    '0xAF3E9eF83B1dc9Db18cD5923e3112F6Cd8bfDAeDD',
]


def yield_api_instances():
    for api_cls in API_CLASSES:
        yield _pytest_param(api_cls())


def _pytest_param(api_inst):
    return pytest.param(api_inst, id=str(api_inst))
