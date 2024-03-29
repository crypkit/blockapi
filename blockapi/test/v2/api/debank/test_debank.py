from decimal import Decimal

from blockapi.utils.address import make_checksum_address
from blockapi.v2.api import DebankApi


def test_build_balance_request_url(debank_api):
    url = debank_api._build_request_url(
        'get_balance',
        address='0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca',
        is_all=True,
    )
    assert (
        url
        == 'https://pro-openapi.debank.com/v1/user/all_token_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca&is_all=True'
    )


def test_build_balance_request_url_with_custom_url():
    api = DebankApi('dummy-key', False, base_url='https://proxy/')

    url = api._build_request_url(
        'get_balance',
        address='0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca',
        is_all=True,
    )
    assert (
        url
        == 'https://proxy/v1/user/all_token_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca&is_all=True'
    )


def test_build_balance_request_url_with_is_all_off(debank_api_all_off):
    url = debank_api_all_off._build_request_url(
        'get_balance',
        address='0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca',
        is_all=False,
    )
    assert (
        url
        == 'https://pro-openapi.debank.com/v1/user/all_token_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca&is_all=False'
    )


def test_build_protocols_request_url(debank_api):
    url = debank_api._build_request_url('get_protocols')
    assert url == 'https://pro-openapi.debank.com/v1/protocol/all_list'


def test_build_portfolio_request_url(debank_api):
    url = debank_api._build_request_url(
        'get_portfolio', address='0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca'
    )
    assert (
        url
        == 'https://pro-openapi.debank.com/v1/user/all_complex_protocol_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca'
    )


def test_error_response_returns_empty_balances(
    debank_api, protocol_cache, error_response_raw, requests_mock
):
    protocol_cache.update({})
    requests_mock.get(
        "https://pro-openapi.debank.com/v1/user/all_token_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca&is_all=true",
        text=error_response_raw,
    )
    parsed_items = debank_api.get_balance("0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca")
    assert parsed_items == []


def test_error_response_logs_error(
    debank_api, protocol_cache, error_response_raw, requests_mock, caplog
):
    protocol_cache.update({})

    requests_mock.get(
        "https://pro-openapi.debank.com/v1/user/all_token_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca&is_all=true",
        text=error_response_raw,
    )
    fetched = debank_api.fetch_balances("0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca")
    parsed = debank_api.parse_balances(fetched)
    expected_error = [
        {
            'error': {
                'id': 'User Address Unknown format '
                '0xca8fa8f0b631ecdb18cda619c4fc9d197c8affc, attempted to '
                'normalize to 0xca8fa8f0b631ecdb18cda619c4fc9d197c8affc'
            },
            'message': 'Input payload validation failed',
        }
    ]

    assert parsed.errors == expected_error


def test_get_balance_has_api_key_header(debank_api, protocol_cache, requests_mock):
    req = requests_mock.get(
        'https://pro-openapi.debank.com/v1/user/all_token_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca&is_all=True',
        text='{}',
    )
    protocol_cache.update({})
    debank_api.get_balance("0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca")
    assert req.last_request.headers.get('AccessKey') == 'dummy-key'


def test_get_portfolio_has_api_key_header(debank_api, protocol_cache, requests_mock):
    req = requests_mock.get(
        'https://pro-openapi.debank.com/v1/user/all_complex_protocol_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca',
        text='{}',
    )
    protocol_cache.update({})
    debank_api.get_portfolio("0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca")
    assert req.last_request.headers.get('AccessKey') == 'dummy-key'


def test_get_protocol(debank_api, requests_mock):
    req = requests_mock.get(
        'https://pro-openapi.debank.com/v1/protocol/all_list',
        text='{}',
    )
    debank_api.get_protocols()
    assert req.last_request.headers.get('AccessKey') == 'dummy-key'


def test_get_chain(debank_api, requests_mock):
    req = requests_mock.get(
        'https://pro-openapi.debank.com/v1/chain/list',
        text='[]',
    )
    debank_api.get_chains()
    assert req.last_request.headers.get('AccessKey') == 'dummy-key'


def test_repr_doesnt_fail(debank_api):
    assert repr(debank_api) == "DebankApi"


def test_debank_parse_protocols(
    debank_api, yflink_protocol_response_raw, yflink_cache_data, requests_mock
):
    requests_mock.get(
        "https://pro-openapi.debank.com/v1/protocol/all_list",
        text=yflink_protocol_response_raw,
    )
    parsed_items = debank_api.get_protocols()
    assert parsed_items == yflink_cache_data


def test_debank_parse_chains(
    debank_api, debank_chain_eth_response_raw, debank_chain_eth, requests_mock
):
    requests_mock.get(
        "https://pro-openapi.debank.com/v1/chain/list",
        json=debank_chain_eth_response_raw,
    )
    parsed_items = debank_api.get_chains()
    assert parsed_items[0] == debank_chain_eth


def test_get_balance_fetches_protocols(
    debank_api,
    yflink_protocol_response_raw,
    coin_with_protocol_response_raw,
    requests_mock,
):
    requests_mock.get(
        "https://pro-openapi.debank.com/v1/protocol/all_list",
        text=yflink_protocol_response_raw,
    )
    requests_mock.get(
        "https://pro-openapi.debank.com/v1/user/all_token_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca&is_all=true",
        text=coin_with_protocol_response_raw,
    )
    debank_api._protocol_cache.invalidate()
    parsed_items = debank_api.get_balance("0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca")
    assert parsed_items[0].protocol.name == "YFLink"


def test_get_balance_uses_correct_url(
    debank_api,
    yflink_protocol_response_raw,
    coin_with_protocol_response_raw,
    requests_mock,
):
    requests_mock.get(
        "https://pro-openapi.debank.com/v1/protocol/all_list",
        text=yflink_protocol_response_raw,
    )
    requests_mock.get(
        "https://pro-openapi.debank.com/v1/user/all_token_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca&is_all=true",
        text=coin_with_protocol_response_raw,
    )
    parsed_items = debank_api.get_balance("0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca")
    assert parsed_items[0].protocol.name == "YFLink"


def test_get_balance_with_all_unset_uses_correct_url(
    debank_api_all_off,
    yflink_protocol_response_raw,
    coin_with_protocol_response_raw,
    requests_mock,
):
    requests_mock.get(
        "https://pro-openapi.debank.com/v1/protocol/all_list",
        text=yflink_protocol_response_raw,
    )
    requests_mock.get(
        "https://pro-openapi.debank.com/v1/user/all_token_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca&is_all=false",
        text=coin_with_protocol_response_raw,
    )
    parsed_items = debank_api_all_off.get_balance(
        "0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca"
    )
    assert parsed_items[0].protocol.name == "YFLink"


def test_get_portfolio_fetches_protocols(
    debank_api, yflink_protocol_response_raw, portfolio_response_raw, requests_mock
):
    requests_mock.get(
        "https://pro-openapi.debank.com/v1/protocol/all_list",
        text=yflink_protocol_response_raw,
    )
    requests_mock.get(
        "https://pro-openapi.debank.com/v1/user/all_complex_protocol_list?id=0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca",
        text=portfolio_response_raw,
    )
    debank_api._protocol_cache.invalidate()
    parsed_items = debank_api.get_portfolio(
        "0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca"
    )
    assert parsed_items[0].items[0].protocol.name == "YFLink"


def test_protocol_cache_is_shared_by_instances():
    one = DebankApi('dummy-key', True)
    two = DebankApi('dummy-key', True)

    assert one._protocol_cache is two._protocol_cache


def test_make_checksum_address():
    non_valid_addr = make_checksum_address("eth")
    assert non_valid_addr is None


def test_get_usage(debank_api, debank_usage_response_raw, requests_mock):
    requests_mock.get(
        'https://pro-openapi.debank.com/v1/account/units',
        text=debank_usage_response_raw,
    )
    usage = debank_api.get_usage()
    assert usage.balance == Decimal('351014')
