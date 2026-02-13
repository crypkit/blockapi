from decimal import Decimal

import pytest

from blockapi.v2.api.debank import (
    DebankApp,
    DebankPrediction,
)
from blockapi.v2.models import BalanceItem, AssetType
from blockapi.v2.coins import COIN_USDC
from blockapi.v2.models import Blockchain


@pytest.fixture
def polymarket_response():
    """Sample response from get_complex_app_list for Polymarket."""
    return [
        {
            "id": "polymarket",
            "name": "Polymarket",
            "site_url": "https://polymarket.com/",
            "logo_url": "https://static.debank.com/image/project/logo_url/app_polymarket/265aca8cef9212e094ef24c71a01c175.png",
            "has_supported_portfolio": True,
            "portfolio_item_list": [
                {
                    "stats": {
                        "asset_usd_value": 290915.13432776055,
                        "debt_usd_value": 0,
                        "net_usd_value": 290915.13432776055,
                    },
                    "asset_dict": {"be0eecf639f4e6a57e375123e46ed7b4": 290595.12768},
                    "asset_token_list": [
                        {
                            "id": "be0eecf639f4e6a57e375123e46ed7b4",
                            "name": "USDC",
                            "symbol": "USDC",
                            "decimals": 6,
                            "logo_url": "https://static.debank.com/image/app_token/logo_url/polymarket/fc98c076b66fa798bcd8755cd859032e.png",
                            "app_id": "polymarket",
                            "price": 1.0011012113324658,
                            "amount": 290595.12768,
                        }
                    ],
                    "update_at": 1768998504.1334498,
                    "name": "Deposit",
                    "detail_types": ["common"],
                    "detail": {
                        "supply_token_list": [
                            {
                                "id": "be0eecf639f4e6a57e375123e46ed7b4",
                                "name": "USDC",
                                "symbol": "USDC",
                                "decimals": 6,
                                "logo_url": "https://static.debank.com/image/app_token/logo_url/polymarket/fc98c076b66fa798bcd8755cd859032e.png",
                                "app_id": "polymarket",
                                "price": 1.0011012113324658,
                                "amount": 290595.12768,
                            }
                        ]
                    },
                    "proxy_detail": {},
                    "position_index": "cash_0x5c23dead9ecf271448411096f349133e0bb9c465",
                },
                {
                    "stats": {
                        "asset_usd_value": 27068.1993,
                        "debt_usd_value": 0,
                        "net_usd_value": 27068.1993,
                    },
                    "asset_dict": {},
                    "asset_token_list": [],
                    "update_at": 1768998504.1336002,
                    "name": "Prediction",
                    "detail_types": ["prediction"],
                    "detail": {
                        "name": "Lighter market cap (FDV) >$1B one day after launch?",
                        "side": "Yes",
                        "amount": 27068.1993,
                        "price": 1,
                        "claimable": True,
                        "event_end_at": None,
                        "is_market_closed": False,
                    },
                    "proxy_detail": {},
                    "position_index": "0x5c23dead9ecf271448411096f349133e0bb9c465_108054592060808479303370270554306028883916458239782628449790057811735078958789",
                },
                {
                    "stats": {
                        "asset_usd_value": 5099.9924519999995,
                        "debt_usd_value": 0,
                        "net_usd_value": 5099.9924519999995,
                    },
                    "asset_dict": {},
                    "asset_token_list": [],
                    "update_at": 1768998504.1336374,
                    "name": "Prediction",
                    "detail_types": ["prediction"],
                    "detail": {
                        "name": "Gensyn FDV above $600M one day after launch?",
                        "side": "Yes",
                        "amount": 19999.9704,
                        "price": 0.255,
                        "claimable": False,
                        "event_end_at": None,
                        "is_market_closed": False,
                    },
                    "proxy_detail": {},
                    "position_index": "0x5c23dead9ecf271448411096f349133e0bb9c465_101101625858935510994152869873088213062714890530116131353411379193297614599911",
                },
            ],
        }
    ]


def test_empty_response(debank_app_parser):
    parsed_apps = debank_app_parser.parse([])
    assert parsed_apps == []


def test_parse_polymarket_app(debank_app_parser, polymarket_response):
    parsed_apps = debank_app_parser.parse(polymarket_response)
    assert len(parsed_apps) == 1

    app = parsed_apps[0]
    assert isinstance(app, DebankApp)
    assert app.app_id == "polymarket"
    assert app.name == "Polymarket"
    assert app.site_url == "https://polymarket.com/"
    assert app.has_supported_portfolio is True


def test_parse_polymarket_deposits(debank_app_parser, polymarket_response):
    """Deposits should be parsed as BalanceItem objects."""

    parsed_apps = debank_app_parser.parse(polymarket_response)
    app = parsed_apps[0]

    # Should have 1 deposit
    assert len(app.deposits) == 1
    deposit = app.deposits[0]

    assert isinstance(deposit, BalanceItem)
    assert deposit.asset_type == AssetType.DEPOSITED
    assert deposit.balance_raw == Decimal("290595.12768")
    assert deposit.coin.symbol == COIN_USDC.symbol
    assert deposit.coin.info.coingecko_id == COIN_USDC.info.coingecko_id


def test_parse_polymarket_predictions(debank_app_parser, polymarket_response):
    """Predictions should be parsed as DebankPrediction objects."""
    parsed_apps = debank_app_parser.parse(polymarket_response)
    app = parsed_apps[0]

    # Should have 2 predictions
    assert len(app.predictions) == 2

    pred1 = app.predictions[0]
    assert isinstance(pred1, DebankPrediction)
    assert (
        pred1.prediction_name == "Lighter market cap (FDV) >$1B one day after launch?"
    )
    assert pred1.side == "Yes"
    assert pred1.amount == Decimal("27068.1993")
    assert pred1.price == Decimal("1")
    assert pred1.usd_value == Decimal("27068.1993")
    assert pred1.claimable is True
    assert pred1.is_market_closed is False
    assert pred1.chain == Blockchain.POLYGON

    pred2 = app.predictions[1]
    assert pred2.prediction_name == "Gensyn FDV above $600M one day after launch?"
    assert pred2.side == "Yes"
    assert pred2.amount == Decimal("19999.9704")
    assert pred2.price == Decimal("0.255")
    assert pred2.claimable is False
    assert pred2.chain == Blockchain.POLYGON


def test_parse_multiple_apps(debank_app_parser):
    """Test parsing multiple apps."""
    response = [
        {
            "id": "polymarket",
            "name": "Polymarket",
            "has_supported_portfolio": True,
            "portfolio_item_list": [
                {
                    "stats": {
                        "asset_usd_value": 100,
                        "debt_usd_value": 0,
                        "net_usd_value": 100,
                    },
                    "name": "Prediction",
                    "detail_types": ["prediction"],
                    "detail": {
                        "name": "Test prediction",
                        "side": "Yes",
                        "amount": 100,
                        "price": 0.5,
                        "claimable": False,
                        "is_market_closed": False,
                    },
                    "position_index": "test_position_index",
                }
            ],
        },
        {
            "id": "hyperliquid",
            "name": "Hyperliquid",
            "has_supported_portfolio": False,
            "portfolio_item_list": [],
        },
    ]

    parsed_apps = debank_app_parser.parse(response)
    assert len(parsed_apps) == 2
    assert parsed_apps[0].app_id == "polymarket"
    assert parsed_apps[1].app_id == "hyperliquid"
