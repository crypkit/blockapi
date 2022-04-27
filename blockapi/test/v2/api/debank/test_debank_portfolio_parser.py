import logging
from datetime import datetime
from decimal import Decimal

import pytest

from blockapi.v2.models import Protocol, DetailType

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
    assert len(parsed_items) == 1


def test_portfolio_parses_protocol(portfolio_parser, portfolio_response, protocol_trader_joe):
    item = portfolio_parser.parse_item(portfolio_response)
    assert item.protocol == protocol_trader_joe


def test_portfolio_parses_items(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_item(portfolio_response)
    assert len(item.items) == 2


def test_portfolio_parses_item_name(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_item(portfolio_response).items[0]
    assert item.name == "Lending"


def test_portfolio_parses_item_last_updated(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_item(portfolio_response).items[0]
    assert item.last_updated == datetime(2022, 4, 26, 10, 51, 1)


def test_portfolio_parses_item_pool_id(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_item(portfolio_response).items[0]
    assert item.pool_id == '0xdc13687554205E5b89Ac783db14bb5bba4A1eDaC'


def test_portfolio_parses_item_detail_types(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_item(portfolio_response).items[0]
    assert item.detail_types == [DetailType.LENDING]


def test_portfolio_stores_raw_item(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_item(portfolio_response).items[0]
    assert item.raw_portfolio is not None


def test_parse_detail_type(portfolio_parser):
    assert portfolio_parser._parse_detail_types(['lending', 'locked']) == [DetailType.LENDING, DetailType.LOCKED]


def test_parse_unknown_detail_type_logs(portfolio_parser, caplog):
    expected_log = ["'dummy' is not a valid DetailType"]
    with caplog.at_level(level=logging.DEBUG):
        assert portfolio_parser._parse_detail_types(['dummy', 'common']) == [DetailType.COMMON]
        assert expected_log == caplog.messages


def test_parse_supply_token_list(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_item(portfolio_response).items[0]
    assert len(item.supply_token_list) == 1


def test_parse_borrow_token_list(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_item(portfolio_response).items[0]
    assert len(item.borrow_token_list) == 3


def test_parse_token_list(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_item(portfolio_response).items[1]
    assert len(item.token_list) == 1


def test_parse_supply_token_list_parses_balance(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse_item(portfolio_response).items[0].supply_token_list[0]
    assert item.balance == Decimal('7579.956374263135')


def test_parse_portfolio(portfolio_parser, complex_portfolio_response):
    parsed_items = portfolio_parser.parse(complex_portfolio_response)
    assert len(parsed_items) == 20
