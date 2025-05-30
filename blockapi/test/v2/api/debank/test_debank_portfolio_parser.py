import logging
from datetime import datetime, timezone
from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_json_file
from blockapi.v2.api.debank import DebankModelPoolItemDetail, DebankModelPortfolioItem
from blockapi.v2.models import AssetType, FetchResult


def test_empty_response(portfolio_parser, empty_response):
    parsed_items = portfolio_parser.parse(empty_response)
    assert parsed_items == []


def test_parse_response(portfolio_parser, portfolio_response):
    parsed_items = portfolio_parser.parse([portfolio_response])
    assert len(parsed_items) == 2


def test_portfolio_parsing(portfolio_parser, portfolio_response, protocol_trader_joe):
    item = portfolio_parser.parse([portfolio_response])[0]
    assert item.protocol == protocol_trader_joe
    assert item.pool_info.pool_id == '0xdc13687554205e5b89ac783db14bb5bba4a1edac'
    assert item.health_rate == Decimal('0.86')
    assert item.locked_until == datetime(2022, 7, 21, 0, 0, tzinfo=timezone.utc)


def test_portfolio_stores_raw_item(portfolio_parser, portfolio_response):
    item = portfolio_parser.parse([portfolio_response])[0].items[0]
    assert item.last_updated == datetime(2020, 12, 11, 23, 10, 59, tzinfo=timezone.utc)
    assert item.balance == Decimal('7579.956374263135')
    assert item.raw is not None
    assert item.asset_type == AssetType.LENDING
    assert item.is_wallet is False


def test_parse_supply_token_list(portfolio_parser, portfolio_response):
    items = portfolio_parser.parse([portfolio_response])[0].items
    filtered = [item for item in items if item.asset_type == AssetType.LENDING]
    for b in filtered:
        assert b.pool_info.pool_id == '0xdc13687554205e5b89ac783db14bb5bba4a1edac'

    assert len(filtered) == 1


def test_portfolio_parses_name(portfolio_parser, portfolio_response):
    pool = portfolio_parser.parse([portfolio_response])[0]
    assert pool.pool_info.name == 'Pool Name'


def test_parse_borrow_token_list(portfolio_parser, portfolio_response):
    items = portfolio_parser.parse([portfolio_response])[0].items
    filtered = [item for item in items if item.asset_type == AssetType.LENDING_BORROW]
    assert len(filtered) == 3

    for b in filtered:
        assert b.pool_info.pool_id == '0xdc13687554205e5b89ac783db14bb5bba4a1edac'


def test_parse_portfolio(portfolio_parser, complex_portfolio_response):
    parsed_items = portfolio_parser.parse(complex_portfolio_response)
    assert len(parsed_items) == 33


def test_parse_position_index_portfolio(
    portfolio_parser, position_index_portfolio_response
):
    parsed_items = portfolio_parser.parse(position_index_portfolio_response)
    assert len(parsed_items) == 3
    assert parsed_items[0].pool_info.position_index == "455893"


def test_parse_asset_type(portfolio_parser):
    assert portfolio_parser._parse_asset_type('Lending') == AssetType.LENDING


def test_parse_asset_type_vesting(portfolio_parser):
    """requires conversion Vested -> vesting"""
    assert portfolio_parser._parse_asset_type('Vested') == AssetType.VESTING


def test_parse_asset_type_liquidity_pool(portfolio_parser):
    """requires conversion: underscore"""
    assert (
        portfolio_parser._parse_asset_type('Liquidity Pool') == AssetType.LIQUIDITY_POOL
    )


def test_parse_unknown_asset_type_logs(portfolio_parser, caplog):
    expected_log = ["'dummy' is not a valid AssetType"]
    with caplog.at_level(level=logging.DEBUG):
        assert portfolio_parser._parse_asset_type('dummy') == AssetType.LOCKED
        assert expected_log == caplog.messages


def test_parse_mutliple_items(portfolio_parser, aave_portfolio_response):
    parsed = portfolio_parser.parse(aave_portfolio_response)
    balances = []
    for item in parsed:
        balances.extend(item.items)

    assert len(balances) == 3

    staked_aave = balances[0]
    assert staked_aave.asset_type == AssetType.STAKED

    staked_aave_reward = balances[1]
    assert staked_aave_reward.asset_type == AssetType.REWARDS


def test_parse_esgmx_items(portfolio_parser, esgmx_portfolio_response):
    parsed = portfolio_parser.parse(esgmx_portfolio_response)
    assert parsed[0].pool_info.tokens == ['esGMX']
    assert parsed[1].pool_info.tokens == ['esGMX']


def test_parse_tokenset(portfolio_parser, tokenset_portfolio_response):
    parsed = portfolio_parser.parse(tokenset_portfolio_response)
    assert parsed[0].pool_info.name == 'BTC2x-FLI'
    assert parsed[0].pool_info.project_id == 'tokensets'
    assert parsed[0].pool_info.adapter_id == 'tokensets_investment2'
    assert parsed[1].pool_info.name == 'ETH2x-FLI'
    assert parsed[1].pool_info.project_id == 'tokensets'
    assert parsed[1].pool_info.adapter_id == 'tokensets_investment2'


def test_parse_pool_names(portfolio_parser, tokenset_portfolio_response):
    parsed = portfolio_parser.parse(tokenset_portfolio_response)
    assert parsed[0].pool_info.tokens == ['USDC', 'WBTC']
    assert parsed[1].pool_info.tokens == ['ETH', 'USDC']


def test_require_pool_or_pool_id():
    with pytest.raises(ValueError, match="either pool or pool_id must have a value"):
        detail = DebankModelPoolItemDetail()

        DebankModelPortfolioItem(
            name='portfolio', detail=detail, pool=None, pool_id=None
        )


def test_portfolio_with_unknown_chain(portfolio_parser, unknown_chain_response):
    parsed = portfolio_parser.parse(unknown_chain_response)
    assert parsed == []


def test_parse_no_error(debank_api):
    debank_api._protocol_cache.update({})
    parsed = debank_api.parse_pools(FetchResult(data={}))
    assert not parsed.errors


@pytest.fixture
def bio_polls():
    return read_json_file("debank/data/bio_pools.json")


def test_parse_pools(debank_api, bio_polls):
    debank_api._protocol_cache.update({})
    parsed = debank_api.parse_pools(FetchResult(data=[bio_polls]))
    assert parsed
    for data_item in parsed.data:
        assert data_item.items

    for data_item in parsed.data:
        for item in data_item.items:
            assert item.balance > Decimal('0')


def test_skip_duplicate_assets(portfolio_parser, duplicates):
    parsed_items = portfolio_parser.parse(duplicates)
    assert len(parsed_items) == 3
    for item in parsed_items:
        assert len(item.items) == 1


@pytest.fixture
def duplicates():
    return read_json_file("debank/data/duplicates.json")
