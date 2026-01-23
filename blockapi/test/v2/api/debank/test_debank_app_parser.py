from decimal import Decimal

import pytest

from blockapi.v2.api.debank import (
    DebankApp,
    DebankAppDeposit,
    DebankPrediction,
)


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


def test_empty_response(app_parser):
    parsed_apps = app_parser.parse([])
    assert parsed_apps == []


def test_parse_polymarket_app(app_parser, polymarket_response):
    parsed_apps = app_parser.parse(polymarket_response)
    assert len(parsed_apps) == 1

    app = parsed_apps[0]
    assert isinstance(app, DebankApp)
    assert app.app_id == "polymarket"
    assert app.name == "Polymarket"
    assert app.site_url == "https://polymarket.com/"
    assert app.has_supported_portfolio is True


def test_parse_polymarket_deposits(app_parser, polymarket_response):
    """Deposits should be parsed as DebankAppDeposit objects."""
    parsed_apps = app_parser.parse(polymarket_response)
    app = parsed_apps[0]

    # Should have 1 deposit
    assert len(app.deposits) == 1
    deposit = app.deposits[0]

    assert isinstance(deposit, DebankAppDeposit)
    assert deposit.name == "Deposit"
    assert deposit.asset_usd_value == Decimal("290915.13432776055")
    assert deposit.debt_usd_value == Decimal("0")
    assert deposit.net_usd_value == Decimal("290915.13432776055")
    assert deposit.position_index == "cash_0x5c23dead9ecf271448411096f349133e0bb9c465"

    # Should have 1 token (USDC)
    assert len(deposit.tokens) == 1
    assert deposit.tokens[0]["symbol"] == "USDC"
    assert deposit.token_symbols == ["USDC"]


def test_parse_polymarket_predictions(app_parser, polymarket_response):
    """Predictions should be parsed as DebankPrediction objects."""
    parsed_apps = app_parser.parse(polymarket_response)
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

    pred2 = app.predictions[1]
    assert pred2.prediction_name == "Gensyn FDV above $600M one day after launch?"
    assert pred2.side == "Yes"
    assert pred2.amount == Decimal("19999.9704")
    assert pred2.price == Decimal("0.255")
    assert pred2.claimable is False


def test_prediction_stores_raw(app_parser, polymarket_response):
    """Predictions should store raw data for debugging."""
    parsed_apps = app_parser.parse(polymarket_response)
    pred = parsed_apps[0].predictions[0]

    assert pred.raw is not None
    assert "stats" in pred.raw
    assert "detail" in pred.raw


def test_parse_multiple_apps(app_parser):
    """Test parsing multiple apps."""
    response = [
        {
            "id": "app1",
            "name": "App 1",
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
                }
            ],
        },
        {
            "id": "app2",
            "name": "App 2",
            "has_supported_portfolio": False,
            "portfolio_item_list": [],
        },
    ]

    parsed_apps = app_parser.parse(response)
    assert len(parsed_apps) == 2
    assert parsed_apps[0].app_id == "app1"
    assert parsed_apps[1].app_id == "app2"
