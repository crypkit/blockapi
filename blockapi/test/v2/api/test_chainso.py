from decimal import Decimal
from unittest.mock import Mock

import pytest
from requests.exceptions import ReadTimeout

from blockapi.test.v2.api.conftest import read_file
from blockapi.test.v2.test_data import ltc_test_address
from blockapi.v2.api import ChainSoLitecoinApi
from blockapi.v2.base import ApiException
from blockapi.v2.models import FetchResult

URL = f'https://sochain.com/api/v3/balance/LTC/{ltc_test_address}'


def test_fetch_balances(requests_mock):
    requests_mock.get(URL, text=read_file('data/chainso_balance_response.json'))
    api = ChainSoLitecoinApi()
    balances = api.get_balance(ltc_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('262.99968329')
    assert balances[0].balance_raw == Decimal('26299968329')
    assert balances[0].coin == api.coin
    assert requests_mock.last_request.timeout == (3.0, 10.0)


@pytest.mark.parametrize('confirmed', ['0.00000000', '0.00000001'])
def test_confirmed_balance_only(requests_mock, confirmed):
    requests_mock.get(
        URL,
        json={
            'status': 'success',
            'data': {'confirmed': confirmed, 'unconfirmed': '12.00000000'},
        },
    )
    balances = ChainSoLitecoinApi().get_balance(ltc_test_address)
    if Decimal(confirmed):
        assert balances[0].balance == Decimal(confirmed)
        assert balances[0].balance_raw == 1
    else:
        assert balances == []


@pytest.mark.parametrize(
    'response',
    [
        None,
        {},
        {'status': 'fail', 'data': {'confirmed': '0'}},
        {'status': 'success', 'data': {}},
        *[
            {'status': 'success', 'data': {'confirmed': value}}
            for value in [None, 'bad', 'NaN', 'Infinity', '-1', '0.000000001']
        ],
    ],
)
def test_invalid_response_is_not_zero(response):
    with pytest.raises(ApiException):
        ChainSoLitecoinApi().parse_balances(FetchResult(data=response))


@pytest.mark.parametrize('status', [429, 502])
def test_http_failure_does_not_retry_or_return_zero(requests_mock, status):
    requests_mock.get(URL, status_code=status, json={'status': 'fail'})
    sleep_provider = Mock()
    api = ChainSoLitecoinApi(sleep_provider=sleep_provider)
    with pytest.raises(ApiException):
        api.get_balance(ltc_test_address)
    assert requests_mock.call_count == 1
    sleep_provider.sleep.assert_not_called()


def test_read_timeout_is_not_zero(requests_mock):
    requests_mock.get(URL, exc=ReadTimeout('stalled'))
    with pytest.raises(ApiException):
        ChainSoLitecoinApi().get_balance(ltc_test_address)
