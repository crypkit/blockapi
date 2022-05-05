import logging
from datetime import datetime
from decimal import Decimal


def test_empty_response(balance_parser, empty_response):
    parsed_items = balance_parser.parse(empty_response)
    assert parsed_items == []


def test_balance_parsers_skips_empty_balances(balance_parser, balances_with_zero_coin_response):
    parsed_items = balance_parser.parse(balances_with_zero_coin_response)
    assert len(parsed_items) == 1


def test_debank_parses_raw_balance(balance_parser, coin_response):
    item = balance_parser.parse_item(coin_response)
    assert item.balance_raw == Decimal(1500000000000000000000)


def test_debank_parses_balance(balance_parser, coin_response):
    item = balance_parser.parse_item(coin_response)
    assert item.balance == Decimal(1500)


def test_debank_parses_last_updated(balance_parser, coin_response):
    item = balance_parser.parse_item(coin_response)
    assert item.last_updated == datetime(2020, 1, 5, 6, 45, 19)


def test_debank_keeps_raw_data(balance_parser, coin_response):
    item = balance_parser.parse_item(coin_response)
    assert item.raw == coin_response


def test_debank_parses_coin_symbol(balance_parser, coin_response):
    item = balance_parser.parse_item(coin_response)
    assert item.coin.symbol == "PYRO"


def test_debank_parses_coin_name(balance_parser, coin_response):
    item = balance_parser.parse_item(coin_response)
    assert item.coin.name == "PYRO Network"


def test_debank_parses_coin_decimals(balance_parser, coin_response):
    item = balance_parser.parse_item(coin_response)
    assert item.coin.decimals == 18


def test_debank_parses_coin_blockchain(balance_parser, coin_response):
    item = balance_parser.parse_item(coin_response)
    assert item.coin.blockchain == 'eth'


def test_debank_parses_coin_address(balance_parser, coin_response):
    item = balance_parser.parse_item(coin_response)
    assert item.coin.address == '0x14409B0Fc5C7f87b5DAd20754fE22d29A3dE8217'


def test_debank_parses_coin_protocol(balance_parser, coin_response):
    item = balance_parser.parse_item(coin_response)
    assert item.protocol is None


def test_parse_balance(balance_parser, balances_response, protocol_cache, yflink_cache_data):
    protocol_cache.update(yflink_cache_data)
    parsed_items = balance_parser.parse(balances_response)
    assert len(parsed_items) == 28


def test_debank_parses_coin_with_protocol(
    balance_parser, coin_with_protocol_response, protocol_yflink, yflink_cache_data
):
    balance_parser._protocols.update(yflink_cache_data)
    item = balance_parser.parse_item(coin_with_protocol_response)
    assert item.protocol == protocol_yflink


def test_debank_parse_protocol_missing_returns_none(
    balance_parser, coin_with_protocol_response
):
    item = balance_parser.parse_item(coin_with_protocol_response)
    assert item.protocol is None


def test_debank_parse_protocol_missing_logs_message(
    balance_parser, coin_with_protocol_response, protocol_yflink, caplog
):
    expected_log = ["Protocol 'yflink' not found."]
    with caplog.at_level(level=logging.DEBUG):
        _ = balance_parser.parse_item(coin_with_protocol_response)
        assert expected_log == caplog.messages
