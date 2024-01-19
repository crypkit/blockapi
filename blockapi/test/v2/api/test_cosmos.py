import pytest

from blockapi.v2.api.cosmos import (
    CosmosApi,
    CosmosCelestiaApi,
    CosmosDydxApi,
    CosmosOsmosisApi,
    CosmosTokenMapLoader,
)
from blockapi.v2.models import UNKNOWN


@pytest.fixture()
def token_loader():
    return CosmosTokenMapLoader()


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


def test_parse_native_tokens(token_loader, mocked_native_token_response, requests_mock):
    requests_mock.get(
        f'https://raw.githubusercontent.com/PulsarDefi/IBC-Token-Data-Cosmos/main/native_token_data.min.json',
        json=mocked_native_token_response,
    )

    token_loader.parse_native_tokens()
    assert token_loader.tokens_map

    assert token_loader.tokens_map['cosmoshub']
    assert "uatom" in token_loader.tokens_map['cosmoshub']

    assert token_loader.tokens_map['dydx']
    assert "adydx" in token_loader.tokens_map['dydx']


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


@pytest.fixture()
def token_loader_with_mocked_data(
    token_loader, mocked_native_token_response, mocked_ibc_response, requests_mock
):
    requests_mock.get(
        token_loader.NATIVE_TOKEN_DATA_JSON,
        json=mocked_native_token_response,
    )

    requests_mock.get(
        token_loader.IBC_DATA_JSON,
        json=mocked_ibc_response,
    )

    assert token_loader.tokens_map  # Force load tokens map
    yield token_loader


def test_parse_ibc_tokens(token_loader_with_mocked_data):
    assert (
        token_loader_with_mocked_data.tokens_map["akash"][
            "ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2"
        ]
        == token_loader_with_mocked_data.tokens_map["cosmoshub"]["uatom"]
    )
    assert (
        token_loader_with_mocked_data.tokens_map["osmosis"][
            "ibc/276EB8E30E8E1673FFDC80DBC79BF864AD83888F455BE970ED06ED5E13A9BEA6"
        ]
        == token_loader_with_mocked_data.tokens_map["dydx"]["adydx"]
    )


@pytest.fixture()
def mocked_ibc_response_cosmoshub_only():
    return {
        "ibc/00255B18FBBC1E36845AAFDCB4CBD460DC45331496A64C2A29CEAFDD3B997B5F__cosmoshub": {
            "chain": "cosmoshub",
            "hash": "00255B18FBBC1E36845AAFDCB4CBD460DC45331496A64C2A29CEAFDD3B997B5F",
            "supply": "3015000000000000000000",
            "path": "transfer/channel-281",
            "origin": {
                "denom": "adydx",
                "chain": "dydx",
            },
        }
    }


def test_parse_ibc_tokens_2(
    token_loader,
    mocked_native_token_response,
    mocked_ibc_response_cosmoshub_only,
    requests_mock,
):
    requests_mock.get(
        token_loader.NATIVE_TOKEN_DATA_JSON,
        json=mocked_native_token_response,
    )
    requests_mock.get(
        token_loader.IBC_DATA_JSON,
        json=mocked_ibc_response_cosmoshub_only,
    )

    assert token_loader.tokens_map

    assert "cosmoshub" in token_loader.tokens_map

    # tokens_map contain native tokens
    assert "uatom" in token_loader.tokens_map["cosmoshub"]
    assert "adydx" not in token_loader.tokens_map["cosmoshub"]

    assert (
        "ibc/00255B18FBBC1E36845AAFDCB4CBD460DC45331496A64C2A29CEAFDD3B997B5F"
        in token_loader.tokens_map["cosmoshub"]
    )


def test_parse_ibc_tokens_no_native(token_loader, mocked_ibc_response, requests_mock):
    requests_mock.get(
        token_loader.NATIVE_TOKEN_DATA_JSON,
        json={},
    )

    requests_mock.get(
        token_loader.IBC_DATA_JSON,
        json=mocked_ibc_response,
    )

    assert token_loader.tokens_map


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
    token_loader,
    mocked_native_token_response,
    mocked_ibc_response_multiple_chains,
    requests_mock,
):
    requests_mock.get(
        token_loader.NATIVE_TOKEN_DATA_JSON,
        json=mocked_native_token_response,
    )

    requests_mock.get(
        token_loader.IBC_DATA_JSON,
        json=mocked_ibc_response_multiple_chains,
    )

    assert token_loader.tokens_map
    assert (
        token_loader.tokens_map['akash'][
            'ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2'
        ]
        == token_loader.tokens_map['cosmoshub']['uatom']
    )


@pytest.mark.vcr()
@pytest.mark.integration
def test_cosmos_get_balance():
    balances = CosmosApi().get_balance('cosmos14s5zljjqtzyl2zfey7ytkllyp0tampkel24qyu')
    assert len(balances) == 17
    assert all([balance.coin != UNKNOWN for balance in balances])


@pytest.mark.vcr()
@pytest.mark.integration
def test_osmosis_get_balance():
    api = CosmosOsmosisApi()
    balances = api.get_balance('osmo1aff76avnwpnk02wxkc6n5xnwasjkgekazvl8xj')
    assert len(balances) == 2
    assert all([balance.coin != UNKNOWN for balance in balances])


@pytest.mark.vcr()
@pytest.mark.integration
def test_dydx_get_balance():
    api = CosmosDydxApi()
    balances = api.get_balance('dydx1aff76avnwpnk02wxkc6n5xnwasjkgekarwznsh')
    assert len(balances) == 4
    assert all([balance.coin != UNKNOWN for balance in balances])


@pytest.mark.vcr()
@pytest.mark.integration
def test_celestia_get_balance():
    api = CosmosCelestiaApi()
    balances = api.get_balance('celestia1aff76avnwpnk02wxkc6n5xnwasjkgekamaa82d')
    assert len(balances) == 1
    assert all([balance.coin != UNKNOWN for balance in balances])


@pytest.mark.vcr()
def test_dissable_mapping():
    api = CosmosDydxApi(
        enable_token_mapping=False,
    )
    balances = api.get_balance('dydx1aff76avnwpnk02wxkc6n5xnwasjkgekarwznsh')
    assert all(
        [True for balance in balances if balance.coin.symbol in ['unknown', 'DYDX']]
    )


@pytest.mark.parametrize(
    "coingecko_id, expected_address",
    [
        (
            "cosmos",
            "ibc/00255B18FBBC1E36845AAFDCB4CBD460DC45331496A64C2A29CEAFDD3B997B5F",
        ),
        (None, "ibc/00255B18FBBC1E36845AAFDCB4CBD460DC45331496A64C2A29CEAFDD3B997B5F"),
    ],
)
def test_map_returns_ibc_always(
    token_loader, coingecko_id, expected_address, requests_mock
):
    requests_mock.get(
        token_loader.NATIVE_TOKEN_DATA_JSON,
        json={
            'uatom__cosmoshub': {
                "name": "Cosmos Hub Atom",
                "chain": "cosmoshub",
                "denom": "uatom",
                "symbol": "ATOM",
                "decimals": 6,
                "description": "The native staking and governance token of the Cosmos Hub.",
                "coingecko_id": coingecko_id,
                "bridge_asset": None,
                "logos": {
                    "png": "https://raw.githubusercontent.com/cosmos/chain-registry/master/cosmoshub/images/atom.png",
                    "svg": "https://raw.githubusercontent.com/cosmos/chain-registry/master/cosmoshub/images/atom.svg",
                },
            },
        },
    )
    requests_mock.get(
        token_loader.IBC_DATA_JSON,
        json={
            "ibc/00255B18FBBC1E36845AAFDCB4CBD460DC45331496A64C2A29CEAFDD3B997B5F__celestia": {
                "chain": "celestia",
                "hash": "00255B18FBBC1E36845AAFDCB4CBD460DC45331496A64C2A29CEAFDD3B997B5F",
                "supply": "3015000000000000000000",
                "path": "transfer/channel-281",
                "origin": {
                    "denom": "uatom",
                    "chain": "cosmoshub",
                },
            }
        },
    )

    api = CosmosCelestiaApi(tokens_map=token_loader.tokens_map)
    token = api.map_or_create_default(
        'ibc/00255B18FBBC1E36845AAFDCB4CBD460DC45331496A64C2A29CEAFDD3B997B5F'
    )

    assert token.address == expected_address
