import pytest

from blockapi.v2.api.cosmos import CosmosApi
from blockapi.v2.models import UNKNOWN


@pytest.fixture()
def cosmos_api():
    return CosmosApi()


@pytest.fixture()
def mocked_native_token_response():
    return {
        "uatom__cosmoshub": {
            "name": "Cosmos Hub Atom",
            "chain": "cosmoshub",
            "denom": "uatom",
            "symbol": "ATOM",
            "decimals": 6,
            "description": "The native staking and governance token of the Cosmos Hub.",
            "coingecko_id": "cosmos",
            "bridge_asset": None,
            "logos": {
                "png": "https://raw.githubusercontent.com/cosmos/chain-registry/master/cosmoshub/images/atom.png",
                "svg": "https://raw.githubusercontent.com/cosmos/chain-registry/master/cosmoshub/images/atom.svg",
            },
        },
        "adydx__dydx": {
            "name": "dYdX",
            "chain": "dydx",
            "denom": "adydx",
            "symbol": "DYDX",
            "decimals": 18,
            "description": "The native staking token of dYdX Protocol.",
            "coingecko_id": "dydx",
            "bridge_asset": None,
            "logos": {
                "png": "https://raw.githubusercontent.com/cosmos/chain-registry/master/dydx/images/dydx.png",
                "svg": "https://raw.githubusercontent.com/cosmos/chain-registry/master/dydx/images/dydx.svg",
            },
        },
    }


def test_parse_native_tokens(cosmos_api, mocked_native_token_response, requests_mock):
    requests_mock.get(
        f'https://raw.githubusercontent.com/PulsarDefi/IBC-Token-Data-Cosmos/main/native_token_data.min.json',
        json=mocked_native_token_response,
    )

    cosmos_api.parse_native_tokens()
    assert cosmos_api.tokens_map
    assert cosmos_api.tokens_map['cosmoshub']
    assert cosmos_api.tokens_map['dydx']


@pytest.fixture()
def mocked_ibc_response():
    return {
        "ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2__akash": {
            "chain": "akash",
            "hash": "27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2",
            "supply": "10269437",
            "path": "transfer/channel-0",
            "origin": {"denom": "uatom", "chain": "cosmoshub"},
        },
        "ibc/276EB8E30E8E1673FFDC80DBC79BF864AD83888F455BE970ED06ED5E13A9BEA6__osmosis": {
            "chain": "osmosis",
            "hash": "276EB8E30E8E1673FFDC80DBC79BF864AD83888F455BE970ED06ED5E13A9BEA6",
            "supply": "10000000000000000",
            "path": "transfer/channel-251/transfer/channel-299",
            "origin": {"denom": "adydx", "chain": "dydx"},
        },
    }


def test_parse_ibc_tokens(
    cosmos_api, mocked_native_token_response, mocked_ibc_response, requests_mock
):
    requests_mock.get(
        cosmos_api.NATIVE_TOKEN_DATA_JSON,
        json=mocked_native_token_response,
    )

    requests_mock.get(
        cosmos_api.IBC_DATA_JSON,
        json=mocked_ibc_response,
    )

    assert cosmos_api.tokens_map
    assert (
        cosmos_api.tokens_map["akash"][
            "ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2"
        ]
        == cosmos_api.tokens_map["cosmoshub"]["uatom"]
    )
    assert (
        cosmos_api.tokens_map["osmosis"][
            "ibc/276EB8E30E8E1673FFDC80DBC79BF864AD83888F455BE970ED06ED5E13A9BEA6"
        ]
        == cosmos_api.tokens_map["dydx"]["adydx"]
    )


def test_parse_ibc_tokens_no_native(cosmos_api, mocked_ibc_response, requests_mock):
    requests_mock.get(
        cosmos_api.NATIVE_TOKEN_DATA_JSON,
        json={},
    )

    requests_mock.get(
        cosmos_api.IBC_DATA_JSON,
        json=mocked_ibc_response,
    )

    assert cosmos_api.tokens_map


@pytest.fixture()
def mocked_ibc_response_multiple_chains():
    return {
        "ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2__akash": {
            "chain": "akash",
            "hash": "27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2",
            "supply": "10269437",
            "path": "transfer/channel-0",
            "origin": {"denom": "uatom", "chain": ["cosmoshub", 'dydx']},
        }
    }


def test_parse_ibc_tokens_multiple_chains(
    cosmos_api,
    mocked_native_token_response,
    mocked_ibc_response_multiple_chains,
    requests_mock,
):
    requests_mock.get(
        cosmos_api.NATIVE_TOKEN_DATA_JSON,
        json=mocked_native_token_response,
    )

    requests_mock.get(
        cosmos_api.IBC_DATA_JSON,
        json=mocked_ibc_response_multiple_chains,
    )

    assert cosmos_api.tokens_map
    assert (
        cosmos_api.tokens_map['akash'][
            'ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2'
        ]
        == cosmos_api.tokens_map['cosmoshub']['uatom']
    )


@pytest.mark.vcr()
@pytest.mark.integration
def test_get_balance(cosmos_api):
    balances = cosmos_api.get_balance('cosmos14s5zljjqtzyl2zfey7ytkllyp0tampkel24qyu')
    assert len(balances) == 17
    assert all([balance.coin != UNKNOWN for balance in balances])
