import logging
from datetime import datetime
from decimal import Decimal

from blockapi.v2.api.debank import DebankModelBalanceItem
from blockapi.v2.models import AssetType, Blockchain


def test_empty_response(balance_parser, empty_response):
    parsed_items = balance_parser.parse(empty_response)
    assert parsed_items == []


def test_balance_parsers_skips_empty_balances(
    balance_parser, balances_with_zero_coin_response
):
    parsed_items = balance_parser.parse(balances_with_zero_coin_response)
    assert len(parsed_items) == 1


def test_balance_parser_parses_data(balance_parser, coin_response):
    item = balance_parser.parse([coin_response])[0]
    assert item.raw == coin_response
    assert item.balance_raw == Decimal(1500000000000000000000)
    assert item.balance == Decimal(1500)
    assert item.last_updated == datetime(2020, 1, 5, 5, 45, 19)
    assert item.asset_type == AssetType.AVAILABLE
    assert item.protocol is None
    assert item.is_wallet


def test_balance_parser_parses_protocol(
    balance_parser, coin_with_protocol_response, protocol_cache, yflink_cache_data
):
    protocol_cache.update(yflink_cache_data)
    item = balance_parser.parse([coin_with_protocol_response])[0]
    assert item.protocol.protocol_id == "yflink"
    assert item.protocol.name == "YFLink"
    assert item.protocol.chain == Blockchain.ETHEREUM
    assert item.protocol.user_deposit == Decimal(1234.5)

    assert item.coin.protocol_id == "yflink"


def test_debank_parses_coin(balance_parser, coin_response):
    item = balance_parser.parse([coin_response])[0]
    assert item.coin.symbol == "PYRO"
    assert item.coin.name == "PYRO Network"
    assert item.coin.decimals == 18
    assert item.coin.blockchain == Blockchain.ETHEREUM
    assert item.coin.address == '0x14409B0Fc5C7f87b5DAd20754fE22d29A3dE8217'


def test_parse_balance(
    balance_parser, balances_response, protocol_cache, yflink_cache_data
):
    protocol_cache.update(yflink_cache_data)
    parsed_items = balance_parser.parse(balances_response)
    assert len(parsed_items) == 28


def test_debank_parses_protocol(
    balance_parser, coin_with_protocol_response, protocol_yflink, yflink_cache_data
):
    balance_parser._protocols.update(yflink_cache_data)
    item = balance_parser.parse([coin_with_protocol_response])[0]
    assert item.protocol == protocol_yflink


def test_debank_parse_protocol_missing_logs_message(
    balance_parser, coin_with_protocol_response, protocol_yflink, caplog
):
    expected_log = ["Protocol 'yflink' not found."]
    with caplog.at_level(level=logging.DEBUG):
        _ = balance_parser.parse([coin_with_protocol_response])
        assert expected_log == caplog.messages


def test_parse_symbol(balance_parser, mist_response):
    balances = balance_parser.parse(mist_response)
    assert balances[0].coin.symbol == "MIST"


def test_map_eth_to_native_coin(balance_parser):
    balance = DebankModelBalanceItem(
        id="eth",
        chain="eth",
        name="Ethereum",
        symbol="ETH",
        decimals=18,
        amount=Decimal(1),
    )

    coin = balance_parser.get_coin(balance, "ETH")
    assert coin.info.coingecko_id == "ethereum"


def test_map_optimism_eth_to_native_coin(balance_parser):
    balance = DebankModelBalanceItem(
        id="op",
        chain="op",
        name="ETH",
        symbol="ETH",
        decimals=18,
        amount=Decimal(1),
        protocol_id='optimism',
    )

    coin = balance_parser.get_coin(balance, "ETH")
    assert coin.info.coingecko_id == "ethereum"
    assert coin.blockchain == Blockchain.OPTIMISM
    assert coin.protocol_id == 'optimism'


def test_map_canto_coin(balance_parser):
    balance = DebankModelBalanceItem(
        id="canto",
        chain="canto",
        name="CANTO",
        symbol="CANTO",
        decimals=18,
        amount=Decimal(1),
    )

    coin = balance_parser.get_coin(balance, "CANTO")
    assert coin.info.coingecko_id == "canto"
    assert coin.blockchain == Blockchain.CANTO


def test_skip_balance_with_unknown_chain(balance_parser):
    balance = DebankModelBalanceItem(
        id="123",
        chain="does-not-exist",
        name="Unknown",
        symbol="SYM",
        decimals=18,
        amount=Decimal(1),
    )

    item = balance_parser.parse_item(balance)
    assert not item
