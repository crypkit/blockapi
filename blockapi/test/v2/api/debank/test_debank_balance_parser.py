import logging
from datetime import datetime
from decimal import Decimal

from blockapi.v2.models import AssetType, Blockchain


def test_empty_response(balance_parser, empty_response):
    parsed_items = balance_parser.parse(empty_response)
    assert parsed_items == []


def test_balance_parsers_skips_empty_balances(balance_parser, balances_with_zero_coin_response):
    parsed_items = balance_parser.parse(balances_with_zero_coin_response)
    assert len(parsed_items) == 1


def test_balance_parser_parses_data(balance_parser, coin_response):
    item = balance_parser.parse_item(coin_response)
    assert item.balance_raw == Decimal(1500000000000000000000)
    assert item.balance == Decimal(1500)
    assert item.last_updated == datetime(2020, 1, 5, 6, 45, 19)
    assert item.asset_type == AssetType.AVAILABLE
    assert item.protocol is None


def test_debank_parses_coin(balance_parser, coin_response):
    item = balance_parser.parse_item(coin_response)
    assert item.raw == coin_response
    assert item.coin.symbol == "PYRO"
    assert item.coin.name == "PYRO Network"
    assert item.coin.decimals == 18
    assert item.coin.blockchain == Blockchain.ETHEREUM
    assert item.coin.address == '0x14409B0Fc5C7f87b5DAd20754fE22d29A3dE8217'


def test_parse_balance(balance_parser, balances_response, protocol_cache, yflink_cache_data):
    protocol_cache.update(yflink_cache_data)
    parsed_items = balance_parser.parse(balances_response)
    assert len(parsed_items) == 28


def test_debank_parses_protocol(
    balance_parser, coin_with_protocol_response, protocol_yflink, yflink_cache_data
):
    balance_parser._protocols.update(yflink_cache_data)
    item = balance_parser.parse_item(coin_with_protocol_response)
    assert item.protocol == protocol_yflink


def test_debank_parse_protocol_missing_logs_message(
    balance_parser, coin_with_protocol_response, protocol_yflink, caplog
):
    expected_log = ["Protocol 'yflink' not found."]
    with caplog.at_level(level=logging.DEBUG):
        _ = balance_parser.parse_item(coin_with_protocol_response)
        assert expected_log == caplog.messages
