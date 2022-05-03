import logging
from datetime import datetime
from decimal import Decimal

from blockapi.v2.models import AssetType

# noinspection PyUnresolvedReferences
from fixtures import (
    protocol_cache,
    balance_parser,
    protocol_parser,
    portfolio_parser,

    empty_response,
    portfolio_response,
    complex_portfolio_response,

    protocol_trader_joe
)


def test_empty_response(portfolio_parser, empty_response):
    parsed_items = portfolio_parser.parse(empty_response)
    assert parsed_items == []


def test_parse_response(portfolio_parser, portfolio_response):
    parsed_items = portfolio_parser.parse([portfolio_response])
    assert len(parsed_items) == 5


def test_portfolio_parses_root_protocol(portfolio_parser, portfolio_response, protocol_trader_joe):
    item = portfolio_parser.parse_items(portfolio_response)
    assert item[0].pool.protocol == protocol_trader_joe


def test_portfolio_parses_items(portfolio_parser, portfolio_response):
    items = portfolio_parser.parse_items(portfolio_response)
    assert len(items) == 5


def test_portfolio_parses_item_last_updated(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_items(portfolio_response)[0]
    assert item.last_updated == datetime(2020, 12, 12, 0, 10, 59)


def test_portfolio_parses_item_pool_id(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_items(portfolio_response)[0]
    assert item.pool.pool_id == '0xdc13687554205E5b89Ac783db14bb5bba4A1eDaC'


def test_portfolio_parses_item_asset_type(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_items(portfolio_response)[0]
    assert item.asset_type == AssetType.LENDING


def test_portfolio_stores_raw_item(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_items(portfolio_response)[0]
    assert item.raw is not None


def test_parse_asset_type(portfolio_parser):
    assert portfolio_parser._parse_asset_type('Lending') == AssetType.LENDING


def test_parse_unknown_asset_type_logs(portfolio_parser, caplog):
    expected_log = ["'dummy' is not a valid AssetType"]
    with caplog.at_level(level=logging.DEBUG):
        assert portfolio_parser._parse_asset_type('dummy') is None
        assert expected_log == caplog.messages


def test_parse_supply_token_list(portfolio_parser, portfolio_response):
    items = portfolio_parser.parse_items(portfolio_response)
    filtered = [item for item in items if item.asset_type == AssetType.LENDING]
    assert len(filtered) == 1


def test_parse_borrow_token_list(portfolio_parser, portfolio_response):
    items = portfolio_parser.parse_items(portfolio_response)
    filtered = [item for item in items if item.asset_type == AssetType.LENDING_BORROW]
    assert len(filtered) == 3


def test_parse_supply_token_list_parses_balance(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_items(portfolio_response)[0]
    assert item.balance == Decimal('7579.956374263135')


def test_parse_supply_token_list_parses_health_rate(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_items(portfolio_response)[0]
    assert item.pool.health_rate == Decimal('0.86')


def test_parse_supply_token_list_parses_locked_until(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_items(portfolio_response)[0]
    assert item.pool.locked_until == datetime(2022, 7, 21, 2, 0)


def test_parse_portfolio(portfolio_parser, complex_portfolio_response):
    parsed_items = portfolio_parser.parse(complex_portfolio_response)
    assert len(parsed_items) == 59
