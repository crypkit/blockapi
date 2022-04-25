import json
import logging
import os.path
import pytest
from decimal import Decimal
from datetime import datetime

from blockapi.v2.api.debank import DebankApi
from blockapi.v2.models import Protocol


@pytest.fixture
def debank_api():
    return DebankApi()


@pytest.fixture
def debank_balances_response():
    json_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'balance_response.json')
    )
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def empty_response():
    return []


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
def zero_coin_response():
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
def yflink_protocol():
    return Protocol.from_api(protocol_id="yflink", chain="eth", name="YFLink")


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
        "tvl": 0
    }]
    """


@pytest.fixture
def list_with_zero_item_response(zero_coin_response, coin_response):
    return [coin_response, zero_coin_response]


@pytest.fixture
def error_response():
    return {
        "errors": {
            "id": 'User Address Unknown format 0xca8fa8f0b631ecdb18cda619c4fc9d197c8affc, attempted to normalize to '
            '0xca8fa8f0b631ecdb18cda619c4fc9d197c8affc'
        },
        "message": "Input payload validation failed",
    }


def test_build_request_url(debank_api):
    url = debank_api._build_request_url(
        'get_balance', address='0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca'
    )
    assert (
        url
        == 'https://openapi.debank.com/v1/user/token_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca&is_all=false'
    )


def test_empty_response(debank_api, empty_response):
    parsed_items = debank_api._parse_items(empty_response)
    assert parsed_items == []


def test_error_response_returns_empty_balances(debank_api, error_response):
    parsed_items = debank_api._parse_items(error_response)
    assert parsed_items == []


def test_error_response_logs_error(debank_api, error_response, caplog):
    expected_log = [
        'Input payload validation failed',
        'User Address Unknown format 0xca8fa8f0b631ecdb18cda619c4fc9d197c8affc, attempted'
        ' to normalize to 0xca8fa8f0b631ecdb18cda619c4fc9d197c8affc',
    ]

    _ = debank_api._parse_items(error_response)
    assert expected_log == caplog.messages


def test_parse_balace_skips_empty_balances(debank_api, list_with_zero_item_response):
    parsed_items = debank_api._parse_items(list_with_zero_item_response)
    assert len(parsed_items) == 1


def test_parse_balance(debank_api, debank_balances_response, yflink_protocol):
    debank_api._protocols = {'yflink': yflink_protocol}
    parsed_items = debank_api._parse_items(debank_balances_response)
    assert len(parsed_items) == 28


def test_repr_doesnt_fail(debank_api):
    assert repr(debank_api) == "DebankApi"


def test_debank_parses_ra_balance(debank_api, coin_response):
    item = debank_api._parse_raw_balance(coin_response)
    assert item.balance_raw == Decimal(1500000000000000000000)


def test_debank_parses_balance(debank_api, coin_response):
    item = debank_api._parse_raw_balance(coin_response)
    assert item.balance == Decimal(1500)


def test_debank_parses_last_updated(debank_api, coin_response):
    item = debank_api._parse_raw_balance(coin_response)
    assert item.last_updated == datetime(2020, 1, 5, 6, 45, 19)


def test_debank_parses_coin_symbol(debank_api, coin_response):
    item = debank_api._parse_raw_balance(coin_response)
    assert item.coin.symbol == "PYRO"


def test_debank_parses_coin_name(debank_api, coin_response):
    item = debank_api._parse_raw_balance(coin_response)
    assert item.coin.name == "PYRO Network"


def test_debank_parses_coin_decimals(debank_api, coin_response):
    item = debank_api._parse_raw_balance(coin_response)
    assert item.coin.decimals == 18


def test_debank_parses_coin_blockchain(debank_api, coin_response):
    item = debank_api._parse_raw_balance(coin_response)
    assert item.coin.blockchain == 'eth'


def test_debank_parses_coin_address(debank_api, coin_response):
    item = debank_api._parse_raw_balance(coin_response)
    assert item.coin.address == '0x14409B0Fc5C7f87b5DAd20754fE22d29A3dE8217'


def test_debank_parses_coin_protocol(debank_api, coin_response):
    item = debank_api._parse_raw_balance(coin_response)
    assert item.protocol is None


def test_debank_parses_coin_with_protocol(
    debank_api, coin_with_protocol_response, yflink_protocol
):
    debank_api._protocols = {'yflink': yflink_protocol}
    item = debank_api._parse_raw_balance(coin_with_protocol_response)
    assert item.protocol == yflink_protocol


def test_debank_parse_protocol_missing_returns_none(
    debank_api, coin_with_protocol_response, yflink_protocol
):
    debank_api._protocols = {'xxx': yflink_protocol}
    item = debank_api._parse_raw_balance(coin_with_protocol_response)
    assert item.protocol is None


def test_debank_parse_protocol_missing_logs_message(
    debank_api, coin_with_protocol_response, yflink_protocol, caplog
):
    expected_log = ["Protocol 'yflink' not found."]
    with caplog.at_level(level=logging.DEBUG):
        debank_api._protocols = {'xxx': yflink_protocol}
        _ = debank_api._parse_raw_balance(coin_with_protocol_response)
        assert expected_log == caplog.messages


def test_debank_fetches_protocols(
    debank_api, yflink_protocol_response_raw, coin_with_protocol_response, requests_mock
):
    requests_mock.get(
        "https://openapi.debank.com/v1/protocol/list", text=yflink_protocol_response_raw
    )
    item = debank_api._parse_raw_balance(coin_with_protocol_response)
    assert item.protocol.name == "YFLink"
