from decimal import Decimal

import pytest
from requests.exceptions import ConnectionError, ReadTimeout

from blockapi.v2.api import BlockonomicsApi
from blockapi.v2.base import ApiException
from blockapi.v2.models import FetchResult

# Deliberately synthetic identifiers: these tests never access a live wallet.
KEY = 'synthetic-api-key'
URL = 'https://www.blockonomics.co/api/balance'


def row(address='synthetic-derived-address', confirmed=123456789, unconfirmed=0):
    return dict(addr=address, confirmed=confirmed, unconfirmed=unconfirmed)


@pytest.mark.parametrize(
    'address', ['synthetic-address', 'xpubSynthetic', 'ypubSynthetic', 'zpubSynthetic']
)
def test_fetch_and_aggregate(requests_mock, address):
    payload = {
        'response': [
            row(confirmed=123456789, unconfirmed=999),
            row('synthetic-change-address', 1, -10),
        ]
    }
    requests_mock.get(URL, json=payload)
    balances = BlockonomicsApi(api_key=KEY).get_balance(address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('1.23456790')
    assert balances[0].raw == payload
    request = requests_mock.last_request
    assert request.headers['Authorization'] == 'Bearer ' + KEY
    assert request.qs == {'addr': [address.lower()]}
    assert KEY not in request.url
    assert request.timeout == (5, 30)


def test_zero_excludes_unconfirmed(requests_mock):
    requests_mock.get(URL, json={'response': [row(confirmed=0, unconfirmed=100)]})
    assert BlockonomicsApi(api_key=KEY).get_balance('synthetic-address') == []


def test_missing_key_does_not_request(requests_mock):
    with pytest.raises(ApiException, match='API key'):
        BlockonomicsApi().get_balance('synthetic-address')
    assert requests_mock.call_count == 0


@pytest.mark.parametrize('address', ['', 'first second', 'first\nsecond'])
def test_reject_batch_input(requests_mock, address):
    with pytest.raises(ApiException, match='Expected one'):
        BlockonomicsApi(api_key=KEY).get_balance(address)
    assert requests_mock.call_count == 0


@pytest.mark.parametrize('status', [401, 403, 429, 500, 502])
def test_http_error_not_zero(requests_mock, status):
    requests_mock.get(URL, status_code=status, json={'message': 'unavailable'})
    with pytest.raises(ApiException):
        BlockonomicsApi(api_key=KEY).get_balance('synthetic-address')


@pytest.mark.parametrize(
    'error', [ConnectionError('disconnected'), ReadTimeout('timeout')]
)
def test_transport_error_not_zero(requests_mock, error):
    requests_mock.get(URL, exc=error)
    with pytest.raises(ApiException):
        BlockonomicsApi(api_key=KEY).get_balance('synthetic-address')


def test_invalid_json(requests_mock):
    requests_mock.get(URL, text='<html>error</html>')
    with pytest.raises(ApiException, match='Invalid JSON'):
        BlockonomicsApi(api_key=KEY).get_balance('synthetic-address')


@pytest.mark.parametrize(
    'data',
    [
        None,
        {},
        [],
        {'response': []},
        {'response': {}},
        {'response': [None]},
        {'response': [{}]},
        {'response': [row(confirmed=True)]},
        {'response': [row(confirmed=-1)]},
        {'response': [row(confirmed='1')]},
        {'response': [row(confirmed=1.5)]},
        {'response': [row(address=None)]},
        {'response': [row(), row()]},
    ],
)
def test_invalid_response_not_zero(data):
    with pytest.raises(ApiException):
        BlockonomicsApi().parse_balances(FetchResult(data=data))


def test_direct_parse_preserves_error():
    with pytest.raises(ApiException, match='unavailable'):
        BlockonomicsApi().parse_balances(FetchResult(errors=['unavailable']))
