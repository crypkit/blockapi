from blockapi.v2.api.debank import DebankApi


def test_build_balance_request_url(debank_api):
    url = debank_api._build_request_url(
        'get_balance', address='0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca'
    )
    assert (
        url
        == 'https://openapi.debank.com/v1/user/token_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca&is_all=false'
    )


def test_build_protocols_request_url(debank_api):
    url = debank_api._build_request_url('get_protocols')
    assert url == 'https://openapi.debank.com/v1/protocol/list'


def test_build_portfolio_request_url(debank_api):
    url = debank_api._build_request_url(
        'get_portfolio', address='0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca'
    )
    assert (
        url
        == 'https://openapi.debank.com/v1/user/complex_protocol_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca'
    )


def test_error_response_returns_empty_balances(debank_api, protocol_cache, error_response_raw, requests_mock):
    protocol_cache.update({})
    requests_mock.get(
        "https://openapi.debank.com/v1/user/token_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca&is_all=false",
        text=error_response_raw
    )
    parsed_items = debank_api.get_balance("0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca")
    assert parsed_items == []


def test_error_response_logs_error(debank_api, protocol_cache, error_response_raw, requests_mock, caplog):
    protocol_cache.update({})
    expected_log = [
        'Input payload validation failed',
        'User Address Unknown format 0xca8fa8f0b631ecdb18cda619c4fc9d197c8affc, attempted'
        ' to normalize to 0xca8fa8f0b631ecdb18cda619c4fc9d197c8affc',
    ]

    requests_mock.get(
        "https://openapi.debank.com/v1/user/token_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca&is_all=false",
        text=error_response_raw
    )
    _ = debank_api.get_balance("0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca")
    assert expected_log == caplog.messages


def test_repr_doesnt_fail(debank_api):
    assert repr(debank_api) == "DebankApi"


def test_debank_parse_protocols(
        debank_api, yflink_protocol_response_raw, yflink_cache_data, requests_mock
):
    requests_mock.get(
        "https://openapi.debank.com/v1/protocol/list", text=yflink_protocol_response_raw
    )
    parsed_items = debank_api.get_protocols()
    assert parsed_items == yflink_cache_data


def test_get_balance_fetches_protocols(
    debank_api, yflink_protocol_response_raw, coin_with_protocol_response_raw, requests_mock
):
    requests_mock.get(
        "https://openapi.debank.com/v1/protocol/list", text=yflink_protocol_response_raw
    )
    requests_mock.get(
        "https://openapi.debank.com/v1/user/token_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca&is_all=false",
        text=coin_with_protocol_response_raw
    )
    debank_api._protocol_cache.invalidate()
    parsed_items = debank_api.get_balance("0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca")
    assert parsed_items[0].protocol.name == "YFLink"


def test_get_portfolio_fetches_protocols(
    debank_api, yflink_protocol_response_raw, portfolio_response_raw, requests_mock
):
    requests_mock.get(
        "https://openapi.debank.com/v1/protocol/list", text=yflink_protocol_response_raw
    )
    requests_mock.get(
        "https://openapi.debank.com/v1/user/complex_protocol_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca",
        text=portfolio_response_raw
    )
    debank_api._protocol_cache.invalidate()
    parsed_items = debank_api.get_portfolio("0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca")
    assert parsed_items[0].items[0].protocol.name == "YFLink"


def test_protocol_cache_is_shared_by_instances():
    one = DebankApi()
    two = DebankApi()

    assert one._protocol_cache is two._protocol_cache
