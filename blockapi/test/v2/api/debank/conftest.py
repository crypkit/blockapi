import os
from typing import List

import pytest

from blockapi.test.v2.api.conftest import read_file, read_json_file
from blockapi.v2.api.debank import (
    DebankApi,
    DebankAppParser,
    DebankBalanceParser,
    DebankChain,
    DebankPortfolioParser,
    DebankProtocolCache,
    DebankProtocolParser,
    DebankUsageParser,
)
from blockapi.v2.coins import COIN_ETH
from blockapi.v2.models import BalanceItem, Blockchain, Pool, PoolInfo, Protocol


@pytest.fixture()
def real_debank_api():
    key = os.environ.get('DEBANK_API_KEY')
    return DebankApi(api_key=key, is_all=False)


@pytest.fixture
def protocol_cache():
    return DebankProtocolCache()


@pytest.fixture
def balance_parser(protocol_cache):
    return DebankBalanceParser(protocol_cache)


@pytest.fixture
def protocol_parser():
    return DebankProtocolParser()


@pytest.fixture
def usage_parser():
    return DebankUsageParser()


@pytest.fixture
def debank_api(protocol_cache):
    return DebankApi('dummy-key', True, protocol_cache)


@pytest.fixture
def debank_api_all_off(protocol_cache):
    return DebankApi('dummy-key', False, protocol_cache)


@pytest.fixture
def portfolio_parser(protocol_parser, balance_parser):
    return DebankPortfolioParser(protocol_parser, balance_parser)


@pytest.fixture
def debank_app_parser():
    return DebankAppParser()


@pytest.fixture
def balance_item():
    return BalanceItem.from_api(
        balance_raw='12340000000000000000',
        coin=COIN_ETH,
        raw={'balance': '12340000000000000000', 'coin': 'eth'},
    )


@pytest.fixture
def pool_item(protocol_yflink, balance_item):
    return Pool.from_api(
        protocol=protocol_yflink,
        items=[balance_item],
        locked_until=1658361600,
        health_rate='0.99',
        pool_info=PoolInfo.from_api(pool_id='123', name='yflink', project_id='yflink'),
    )


@pytest.fixture
def empty_response():
    return []


@pytest.fixture
def error_response_raw():
    return '''{
        "errors": {
            "id": "User Address Unknown format 0xca8fa8f0b631ecdb18cda619c4fc9d197c8affc, attempted to normalize to 0xca8fa8f0b631ecdb18cda619c4fc9d197c8affc"
        },
        "message": "Input payload validation failed"
    }
    '''


@pytest.fixture
def balances_response() -> List:
    return read_json_file("debank/data/balance_response.json")


@pytest.fixture
def complex_portfolio_response() -> List:
    return read_json_file("debank/data/complex_portfolio_response.json")


@pytest.fixture
def position_index_portfolio_response() -> List:
    return read_json_file("debank/data/position_index_portfolio_response.json")


@pytest.fixture
def aave_portfolio_response() -> List:
    return read_json_file("debank/data/aave_portfolio_response.json")


@pytest.fixture
def esgmx_portfolio_response() -> List:
    return read_json_file("debank/data/esgmx_portfolio_response.json")


@pytest.fixture
def tokenset_portfolio_response() -> List:
    return read_json_file("debank/data/tokenset_portfolio_response.json")


@pytest.fixture
def mist_response() -> List:
    return read_json_file("debank/data/mist_response.json")


@pytest.fixture
def unknown_chain_response() -> dict:
    return read_json_file('debank/data/unknown_chain_response.json')


@pytest.fixture
def debank_usage_response() -> dict:
    return read_json_file('debank/data/usage_response.json')


@pytest.fixture
def debank_usage_response_raw() -> str:
    return read_file('debank/data/usage_response.json')


@pytest.fixture
def portfolio_response():
    return {
        "id": "avax_traderjoexyz_lending",
        "chain": "avax",
        "name": "Trader Joe Lending",
        "site_url": "https://www.traderjoexyz.com",
        "logo_url": "https://static.debank.com/image/project/logo_url/avax_traderjoexyz_lending"
        "/eab9fd6fb47852d3b7766515bfefe366.png",
        "has_supported_portfolio": True,
        "tvl": 162476998.75607753,
        "portfolio_item_list": [
            {
                "stats": {
                    "asset_usd_value": 547045.4515305705,
                    "debt_usd_value": 0,
                    "net_usd_value": 547045.4515305705,
                },
                "update_at": 1650963061.376993,
                "name": "Lending",
                "pool_id": "0xdc13687554205e5b89ac783db14bb5bba4a1edac",
                "detail_types": ["lending"],
                "detail": {
                    "description": "Pool Name",
                    "supply_token_list": [
                        {
                            "id": "0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7",
                            "chain": "avax",
                            "name": "Wrapped AVAX",
                            "symbol": "WAVAX",
                            "display_symbol": "WAVAX",
                            "optimized_symbol": "WAVAX",
                            "decimals": 18,
                            "logo_url": "https://static.debank.com/image/avax_token/logo_url/0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7/753d82f0137617110f8dec56309b4065.png",
                            "protocol_id": "avax_gmx",
                            "price": 72.17,
                            "is_verified": True,
                            "is_core": True,
                            "is_wallet": True,
                            "time_at": 1607728259,
                            "amount": 7579.956374263135,
                            "is_collateral": False,
                        }
                    ],
                    "borrow_token_list": [
                        {
                            "id": "0x865377367054516e17014ccded1e7d814edc9ce4",
                            "chain": "eth",
                            "name": "Dola USD Stablecoin",
                            "symbol": "DOLA",
                            "display_symbol": None,
                            "optimized_symbol": "DOLA",
                            "decimals": 18,
                            "logo_url": "https://static.debank.com/image/eth_token/logo_url/0x865377367054516e17014ccded1e7d814edc9ce4/cf89c85a0a6b374247c072fe3131bacb.png",
                            "protocol_id": "",
                            "price": 1,
                            "is_verified": True,
                            "is_core": True,
                            "is_wallet": True,
                            "time_at": 1614116357,
                            "amount": 661077.3612934694,
                        },
                        {
                            "id": "eth",
                            "chain": "eth",
                            "name": "ETH",
                            "symbol": "ETH",
                            "display_symbol": None,
                            "optimized_symbol": "ETH",
                            "decimals": 18,
                            "logo_url": "https://static.debank.com/image/token/logo_url/eth/935ae4e4d1d12d59a99717a24f2540b5.png",
                            "protocol_id": "",
                            "price": 2996.56,
                            "is_verified": True,
                            "is_core": True,
                            "is_wallet": True,
                            "time_at": 1483200000,
                            "amount": 2.97837275242947,
                        },
                        {
                            "id": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
                            "chain": "eth",
                            "name": "Wrapped BTC",
                            "symbol": "WBTC",
                            "display_symbol": None,
                            "optimized_symbol": "WBTC",
                            "decimals": 8,
                            "logo_url": "https://static.debank.com/image/eth_token/logo_url/0x2260fac5e5542a773aa44fbcfedf7c193bc2c599/d3c52e7c7449afa8bd4fad1c93f50d93.png",
                            "protocol_id": "",
                            "price": 40460.15,
                            "is_verified": True,
                            "is_core": True,
                            "is_wallet": True,
                            "time_at": 1543095952,
                            "amount": 5.3e-7,
                        },
                    ],
                    "health_rate": 0.86,
                    "unlock_at": 1658361600,
                },
                "proxy_detail": {},
            },
            {
                "stats": {
                    "asset_usd_value": 220.67854479949355,
                    "debt_usd_value": 0,
                    "net_usd_value": 220.67854479949355,
                },
                "update_at": 1650963061.3988287,
                "name": "Rewards",
                "pool_id": "0xdc13687554205e5b89ac783db14bb5bba4a1edac",
                "detail_types": ["reward"],
                "detail": {
                    "token_list": [
                        {
                            "id": "0x6e84a6216ea6dacc71ee8e6b0a5b7322eebc0fdd",
                            "chain": "avax",
                            "name": "JoeToken",
                            "symbol": "JOE",
                            "display_symbol": None,
                            "optimized_symbol": "JOE",
                            "decimals": 18,
                            "logo_url": "https://static.debank.com/image/avax_token/logo_url"
                            "/0x6e84a6216ea6dacc71ee8e6b0a5b7322eebc0fdd/25f094b523a2d6c51e084eeb8f60dd2f"
                            ".png",
                            "protocol_id": "avax_traderjoexyz_lending",
                            "price": 1.0898007248925483,
                            "is_verified": True,
                            "is_core": True,
                            "is_wallet": True,
                            "time_at": 1624780261,
                            "amount": 202.49440081924328,
                        }
                    ]
                },
                "proxy_detail": {},
            },
        ],
    }


@pytest.fixture
def portfolio_response_raw():
    return """[{
        "id": "avax_traderjoexyz_lending",
        "chain": "avax",
        "name": "Trader Joe Lending",
        "site_url": "https://www.traderjoexyz.com",
        "logo_url": "https://static.debank.com/image/project/logo_url/avax_traderjoexyz_lending/eab9fd6fb47852d3b7766515bfefe366.png",
        "has_supported_portfolio": true,
        "tvl": 162476998.75607753,
        "portfolio_item_list": [
            {
                "stats": {
                    "asset_usd_value": 547045.4515305705,
                    "debt_usd_value": 0,
                    "net_usd_value": 547045.4515305705
                },
                "update_at": 1650963061.376993,
                "name": "Lending",
                "pool_id": "0xdc13687554205e5b89ac783db14bb5bba4a1edac",
                "detail_types": [
                    "lending"
                ],
                "detail": {
                    "supply_token_list": [
                        {
                            "id": "0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7",
                            "chain": "avax",
                            "name": "Wrapped AVAX",
                            "symbol": "WAVAX",
                            "display_symbol": "WAVAX",
                            "optimized_symbol": "WAVAX",
                            "decimals": 18,
                            "logo_url": "https://static.debank.com/image/avax_token/logo_url/0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7/753d82f0137617110f8dec56309b4065.png",
                            "protocol_id": "yflink",
                            "price": 72.17,
                            "is_verified": true,
                            "is_core": true,
                            "is_wallet": true,
                            "time_at": 1607728259,
                            "amount": 7579.956374263135,
                            "is_collateral": false
                        }
                    ],
                    "borrow_token_list": [
                        {
                            "id": "0x865377367054516e17014ccded1e7d814edc9ce4",
                            "chain": "eth",
                            "name": "Dola USD Stablecoin",
                            "symbol": "DOLA",
                            "display_symbol": null,
                            "optimized_symbol": "DOLA",
                            "decimals": 18,
                            "logo_url": "https://static.debank.com/image/eth_token/logo_url/0x865377367054516e17014ccded1e7d814edc9ce4/cf89c85a0a6b374247c072fe3131bacb.png",
                            "protocol_id": "",
                            "price": 1,
                            "is_verified": true,
                            "is_core": true,
                            "is_wallet": true,
                            "time_at": 1614116357,
                            "amount": 661077.3612934694
                        },
                        {
                            "id": "eth",
                            "chain": "eth",
                            "name": "ETH",
                            "symbol": "ETH",
                            "display_symbol": null,
                            "optimized_symbol": "ETH",
                            "decimals": 18,
                            "logo_url": "https://static.debank.com/image/token/logo_url/eth/935ae4e4d1d12d59a99717a24f2540b5.png",
                            "protocol_id": "",
                            "price": 2996.56,
                            "is_verified": true,
                            "is_core": true,
                            "is_wallet": true,
                            "time_at": 1483200000,
                            "amount": 2.97837275242947
                        },
                        {
                            "id": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
                            "chain": "eth",
                            "name": "Wrapped BTC",
                            "symbol": "WBTC",
                            "display_symbol": null,
                            "optimized_symbol": "WBTC",
                            "decimals": 8,
                            "logo_url": "https://static.debank.com/image/eth_token/logo_url/0x2260fac5e5542a773aa44fbcfedf7c193bc2c599/d3c52e7c7449afa8bd4fad1c93f50d93.png",
                            "protocol_id": "",
                            "price": 40460.15,
                            "is_verified": true,
                            "is_core": true,
                            "is_wallet": true,
                            "time_at": 1543095952,
                            "amount": 5.3e-7
                        }
                    ],
                    "health_rate": null
                },
                "proxy_detail": {}
            },
            {
                "stats": {
                    "asset_usd_value": 220.67854479949355,
                    "debt_usd_value": 0,
                    "net_usd_value": 220.67854479949355
                },
                "update_at": 1650963061.3988287,
                "name": "Rewards",
                "pool_id": "0xdc13687554205e5b89ac783db14bb5bba4a1edac",
                "detail_types": [
                    "reward"
                ],
                "detail": {
                    "token_list": [
                        {
                            "id": "0x6e84a6216ea6dacc71ee8e6b0a5b7322eebc0fdd",
                            "chain": "avax",
                            "name": "JoeToken",
                            "symbol": "JOE",
                            "display_symbol": null,
                            "optimized_symbol": "JOE",
                            "decimals": 18,
                            "logo_url": "https://static.debank.com/image/avax_token/logo_url/0x6e84a6216ea6dacc71ee8e6b0a5b7322eebc0fdd/25f094b523a2d6c51e084eeb8f60dd2f.png",
                            "protocol_id": "avax_traderjoexyz_lending",
                            "price": 1.0898007248925483,
                            "is_verified": true,
                            "is_core": true,
                            "is_wallet": true,
                            "time_at": 1624780261,
                            "amount": 202.49440081924328
                        }
                    ]
                },
                "proxy_detail": {}
            }
        ]
    }]
    """


@pytest.fixture
def balances_with_zero_coin_response(coin_with_zero_amount_response, coin_response):
    return [coin_response, coin_with_zero_amount_response]


@pytest.fixture
def coin_response():
    return {
        "id": "0x14409b0fc5c7f87b5dad20754fe22d29a3de8217",
        "chain": "eth",
        "name": "PYRO Network",
        "symbol": "PYRO",
        "display_symbol": None,
        "optimized_symbol": "PYRO",
        "decimals": 18,
        "logo_url": "https://static.debank.com/image/eth_token/logo_url/0x14409b0fc5c7f87b5dad20754fe22d29a3de8217"
        "/12f825ee65922435c9ed553d1ce6ad95.png",
        "protocol_id": "",
        "price": 0,
        "is_verified": True,
        "is_core": True,
        "is_wallet": True,
        "time_at": 1578203119,
        "amount": 1500,
        "raw_amount": 1.5e21,
        "raw_amount_hex_str": "0x5150ae84a8cdf00000",
    }


@pytest.fixture
def coin_with_zero_amount_response():
    return {
        "id": "0x14409b0fc5c7f87b5dad20754fe22d29a3de8217",
        "chain": "eth",
        "name": "PYRO Network",
        "symbol": "PYRO",
        "display_symbol": None,
        "optimized_symbol": "PYRO",
        "decimals": 18,
        "logo_url": "https://static.debank.com/image/eth_token/logo_url/0x14409b0fc5c7f87b5dad20754fe22d29a3de8217"
        "/12f825ee65922435c9ed553d1ce6ad95.png",
        "protocol_id": "",
        "price": 0,
        "is_verified": True,
        "is_core": True,
        "is_wallet": True,
        "time_at": 1578203119,
        "amount": 0,
        "raw_amount": 0,
        "raw_amount_hex_str": "0x0",
    }


@pytest.fixture
def coin_with_protocol_response():
    return {
        "id": "0x28cb7e841ee97947a86b06fa4090c8451f64c0be",
        "chain": "eth",
        "name": "YFLink",
        "symbol": "YFL",
        "display_symbol": None,
        "optimized_symbol": "YFL",
        "decimals": 18,
        "logo_url": "https://static.debank.com/image/eth_token/logo_url/0x28cb7e841ee97947a86b06fa4090c8451f64c0be"
        "/df942140382c5b492c7ffe3419010b49.png",
        "protocol_id": "yflink",
        "price": 0,
        "is_verified": True,
        "is_core": True,
        "is_wallet": True,
        "time_at": 1596432467,
        "amount": 0.000069,
        "raw_amount": 69000000000000,
        "raw_amount_hex_str": "0x3ec1507d5000",
    }


@pytest.fixture
def coin_with_protocol_response_raw():
    return '''[{
        "id": "0x28cb7e841ee97947a86b06fa4090c8451f64c0be",
        "chain": "eth",
        "name": "YFLink",
        "symbol": "YFL",
        "display_symbol": null,
        "optimized_symbol": "YFL",
        "decimals": 18,
        "logo_url": "https://static.debank.com/image/eth_token/logo_url/0x28cb7e841ee97947a86b06fa4090c8451f64c0be/df942140382c5b492c7ffe3419010b49.png",
        "protocol_id": "yflink",
        "price": 0,
        "is_verified": true,
        "is_core": true,
        "is_wallet": true,
        "time_at": 1596432467,
        "amount": 0.000069,
        "raw_amount": 69000000000000,
        "raw_amount_hex_str": "0x3ec1507d5000"
    }]'''


@pytest.fixture
def yflink_protocol_response():
    return [
        {
            "id": "yflink",
            "chain": "eth",
            "name": "YFLink",
            "site_url": "https://linkswap.app",
            "logo_url": "https://static.debank.com/image/project/logo_url/yflink/a43f4e05d96b559fecf4984f760bf737.png",
            "has_supported_portfolio": False,
            "tvl": 1234.5,
        }
    ]


@pytest.fixture
def yflink_protocol_response_raw():
    return """
    [{
        "id": "yflink",
        "chain": "eth",
        "name": "YFLink",
        "site_url": "https://linkswap.app",
        "logo_url": "https://static.debank.com/image/project/logo_url/yflink/a43f4e05d96b559fecf4984f760bf737.png",
        "has_supported_portfolio": false,
        "tvl": 1234.5
    }]
    """


@pytest.fixture
def protocol_yflink():
    return Protocol.from_api(
        protocol_id="yflink",
        chain=Blockchain.ETHEREUM,
        name="YFLink",
        user_deposit=1234.5,
        site_url="https://linkswap.app",
        logo_url="https://static.debank.com/image/project/logo_url/yflink/a43f4e05d96b559fecf4984f760bf737.png",
    )


@pytest.fixture
def protocol_trader_joe():
    return Protocol.from_api(
        protocol_id="avax_traderjoexyz_lending",
        chain=Blockchain.AVALANCHE,
        name="Trader Joe Lending",
        user_deposit='162476998.75607753',
        site_url="https://www.traderjoexyz.com",
        logo_url="https://static.debank.com/image/project/logo_url/avax_traderjoexyz_lending"
        "/eab9fd6fb47852d3b7766515bfefe366.png",
        has_supported_portfolio=True,
    )


@pytest.fixture
def yflink_cache_data(protocol_yflink):
    return {'yflink': protocol_yflink}


@pytest.fixture
def debank_chain_eth_response_raw():
    return [
        {
            "id": "eth",
            "community_id": 1,
            "name": "Ethereum",
            "native_token_id": "eth",
            "logo_url": "https://static.debank.com/image/chain/logo_url/eth/"
            "42ba589cd077e7bdd97db6480b0ff61d.png",
            "wrapped_token_id": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            "is_support_pre_exec": True,
        }
    ]


@pytest.fixture
def debank_chain_eth():
    return DebankChain(
        chain=Blockchain.ETHEREUM,
        community_id=1,
        name='Ethereum',
        logo_url="https://static.debank.com/image/chain/logo_url/eth/"
        "42ba589cd077e7bdd97db6480b0ff61d.png",
    )
