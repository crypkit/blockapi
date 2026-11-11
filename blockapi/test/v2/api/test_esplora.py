from decimal import Decimal

import pytest
from requests.exceptions import ConnectionError, ReadTimeout

from blockapi.v2.api import EsploraApi, MempoolSpaceApi
from blockapi.v2.base import ApiException
from blockapi.v2.models import FetchResult

ADDRESS = '17vu4hEWtuPXFbJLPKtg4MFQnoohRE88v6'


def response(funded=400000, spent=108101):
    return {
        'address': ADDRESS,
        'chain_stats': {'funded_txo_sum': funded, 'spent_txo_sum': spent},
        'mempool_stats': {'funded_txo_sum': 999999, 'spent_txo_sum': 123},
    }


@pytest.mark.parametrize(
    'api',
    [
        EsploraApi(),
        MempoolSpaceApi(),
        EsploraApi(base_url='https://example.com/btc/api'),
    ],
)
def test_confirmed_balance_and_endpoint(requests_mock, api):
    requests_mock.get(api.base_url + 'address/' + ADDRESS, json=response())
    balances = api.get_balance(ADDRESS)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('0.00291899')
    assert balances[0].raw == response()
    assert requests_mock.last_request.timeout == (5, 15)


def test_zero_confirmed_balance_ignores_mempool(requests_mock):
    api = EsploraApi()
    requests_mock.get(api.base_url + 'address/' + ADDRESS, json=response(100, 100))
    assert api.get_balance(ADDRESS) == []


@pytest.mark.parametrize('prefix', ['xpub', 'ypub', 'zpub', 'tpub', 'upub', 'vpub'])
def test_extended_key_rejected_without_http(requests_mock, prefix):
    with pytest.raises(ApiException, match='extended public keys'):
        EsploraApi().get_balance(prefix + 'example')
    assert requests_mock.call_count == 0


@pytest.mark.parametrize('status', [400, 429, 500, 503])
def test_http_failure_is_not_zero_balance(requests_mock, status):
    api = EsploraApi()
    requests_mock.get(api.base_url + 'address/' + ADDRESS, status_code=status)
    with pytest.raises(ApiException):
        api.get_balance(ADDRESS)


@pytest.mark.parametrize('error', [ConnectionError('refused'), ReadTimeout('timeout')])
def test_network_failure_is_not_zero_balance(requests_mock, error):
    api = EsploraApi()
    requests_mock.get(api.base_url + 'address/' + ADDRESS, exc=error)
    with pytest.raises(ApiException):
        api.get_balance(ADDRESS)


def test_invalid_json_is_fetch_error(requests_mock):
    api = EsploraApi()
    requests_mock.get(
        api.base_url + 'address/' + ADDRESS, text='<html>unavailable</html>'
    )
    with pytest.raises(ApiException, match='Invalid JSON'):
        api.get_balance(ADDRESS)


@pytest.mark.parametrize(
    'data',
    [
        None,
        {},
        [],
        {'chain_stats': {}},
        response(-1, 0),
        response(0, 1),
        response('100', 0),
        response(True, 0),
        response(1.5, 0),
    ],
)
def test_malformed_totals_are_not_zero_balance(data):
    with pytest.raises(ApiException, match='Invalid Esplora response'):
        EsploraApi().parse_balances(FetchResult(data=data))


def test_direct_parse_preserves_fetch_error():
    with pytest.raises(ApiException, match='unavailable'):
        EsploraApi().parse_balances(FetchResult(errors=['unavailable']))
