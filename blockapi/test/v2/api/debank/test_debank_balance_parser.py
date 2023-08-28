import logging
from datetime import datetime, timezone
from decimal import Decimal

import pytest

from blockapi.v2.api.debank import DebankModelBalanceItem
from blockapi.v2.coins import (
    COIN_ASTR,
    COIN_AURORA,
    COIN_AURORA_AETH,
    COIN_AVAX,
    COIN_AXIE_RON,
    COIN_BNB,
    COIN_BOBA,
    COIN_BTT,
    COIN_CANTO,
    COIN_CELO,
    COIN_CRO,
    COIN_ETH,
    COIN_FTM,
    COIN_FUSE,
    COIN_GLMR,
    COIN_IOTX,
    COIN_KCS,
    COIN_KLAY,
    COIN_MATIC,
    COIN_METIS,
    COIN_MOVR,
    COIN_OKT,
    COIN_ONE,
    COIN_OP,
    COIN_PERP,
    COIN_RON,
    COIN_RSK,
    COIN_SGB,
    COIN_TLOS,
    COIN_WAN,
    COIN_XDAI,
)
from blockapi.v2.models import AssetType, Blockchain, CoingeckoId


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
    assert item.last_updated == datetime(2020, 1, 5, 5, 45, 19, tzinfo=timezone.utc)
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


def test_parse_alchymist_symbol(balance_parser, mist_response):
    balances = balance_parser.parse(mist_response)
    assert balances[0].coin.symbol == "MIST"


def test_get_coin_returns_defined_coin(balance_parser):
    balance = DebankModelBalanceItem(
        id="eth",
        chain="eth",
        name="Ethereum",
        symbol="ETH",
        decimals=18,
        amount=Decimal(1),
    )

    coin = balance_parser.get_coin(balance)
    assert coin is COIN_ETH


def test_get_coin_preserves_protocol_id(balance_parser):
    balance = DebankModelBalanceItem(
        id="eth",
        chain="eth",
        name="Ethereum",
        symbol="ETH",
        decimals=18,
        amount=Decimal(1),
        protocol_id='check_protocol',
    )

    coin = balance_parser.get_coin(balance)
    assert coin.protocol_id == 'check_protocol'
    assert coin.info.coingecko_id == CoingeckoId.ETHEREUM


def test_get_coin_creates_know_coin_allowed_blockchains(balance_parser):
    balance = DebankModelBalanceItem(
        id="op",
        chain="op",
        name="ETH",
        symbol="ETH",
        decimals=18,
        amount=Decimal(1),
        protocol_id='optimism',
    )

    coin = balance_parser.get_coin(balance)
    assert coin.symbol == 'ETH'
    assert coin.blockchain == Blockchain.OPTIMISM
    assert coin.info.coingecko_id == CoingeckoId.ETHEREUM
    assert coin.protocol_id == 'optimism'
    assert coin.address == 'op'


def test_get_coin_creates_unknown_coin(balance_parser):
    balance = DebankModelBalanceItem(
        id="0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7",
        chain="avax",
        name="Wrapped AVAX",
        symbol="WAVAX",
        decimals=18,
        amount=Decimal(1),
        protocol_id='avax_gmx',
    )

    coin = balance_parser.get_coin(balance)
    assert coin.symbol == 'WAVAX'
    assert coin.blockchain == Blockchain.AVALANCHE
    assert not coin.info.coingecko_id
    assert coin.protocol_id == 'avax_gmx'
    assert coin.address == '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7'


@pytest.mark.parametrize(
    ['contract', 'symbol', 'coin'],
    [
        ('aurora', COIN_AURORA.symbol, COIN_AURORA),
        ('eth', COIN_ETH.symbol, COIN_ETH),
        ('eth', COIN_PERP.symbol, COIN_PERP),
        ('aurora', COIN_AURORA_AETH.symbol, COIN_AURORA_AETH),
        ('astar', COIN_ASTR.symbol, COIN_ASTR),
        ('avax', COIN_AVAX.symbol, COIN_AVAX),
        ('bsc', COIN_BNB.symbol, COIN_BNB),
        ('boba', COIN_BOBA.symbol, COIN_BOBA),
        ('btt', COIN_BTT.symbol, COIN_BTT),
        ('canto', COIN_CANTO.symbol, COIN_CANTO),
        ('celo', COIN_CELO.symbol, COIN_CELO),
        ('cro', COIN_CRO.symbol, COIN_CRO),
        ('ftm', COIN_FTM.symbol, COIN_FTM),
        ('fuse', COIN_FUSE.symbol, COIN_FUSE),
        ('hmy', COIN_ONE.symbol, COIN_ONE),
        ('iotex', COIN_IOTX.symbol, COIN_IOTX),
        ('kcc', COIN_KCS.symbol, COIN_KCS),
        ('klay', COIN_KLAY.symbol, COIN_KLAY),
        ('matic', COIN_MATIC.symbol, COIN_MATIC),
        ('ron', COIN_RON.symbol, COIN_RON),
        ('metis', COIN_METIS.symbol, COIN_METIS),
        ('mobm', COIN_GLMR.symbol, COIN_GLMR),
        ('movr', COIN_MOVR.symbol, COIN_MOVR),
        ('okt', COIN_OKT.symbol, COIN_OKT),
        ('op', COIN_OP.symbol, COIN_OP),
        ('rsk', COIN_RSK.symbol, COIN_RSK),
        ('sgb', COIN_SGB.symbol, COIN_SGB),
        ('xdai', COIN_XDAI.symbol, COIN_XDAI),
        ('tlos', COIN_TLOS.symbol, COIN_TLOS),
        ('wan', COIN_WAN.symbol, COIN_WAN),
    ],
)
def test_all_mapping(contract, symbol, coin, balance_parser):
    balance = DebankModelBalanceItem(
        id=contract,
        chain=contract,
        name=symbol,
        symbol=symbol,
        decimals=18,
        amount=Decimal(1),
    )

    assert coin == balance_parser.get_coin(balance)


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
