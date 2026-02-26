from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api.haskoin import HaskoinApi, _to_xpub
from blockapi.v2.base import ApiException
from blockapi.v2.models import FetchResult

# noinspection SpellCheckingInspection
btc_test_address = '35hK24tcLEWcgNA4JxpvbkNkoAcDGqQPsP'
# noinspection SpellCheckingInspection
xpub_test_address = 'xpub6CUGRUonZSQ4TWtTMmzXdrXDtypWKiKrhko4egpiMZbpiaQL2jkwSB1icqYh2cfDfVxdx4df189oLKnC5fSwqPfgyP3hooxujYzAu3fDVmz'
# noinspection SpellCheckingInspection
# ypub/zpub derived from xpub_test_address by swapping version bytes
ypub_test_address = 'ypub6XJXj9Uhi7wYJp5aC8n9qwcj4wxxGLKMcsKHS5ibjZyhmgDZHPvW4Efre3WH2XK9595ShYEDTnWMDcPkoMrxddMHqik8PinQ1H3pHbCYAtS'
# noinspection SpellCheckingInspection
zpub_test_address = 'zpub6r8o2p9croV2A7Gh2VZn42iEEv7QCxJrXyqWDUcV7aMapn2nY464gJKzfFTs2Ry4UnCFT1pmvSru6u1KX4GyRs2ti4SYydbtH17Tg8wL57f'


def test_fetch_balances(requests_mock, haskoin_balance_response):
    requests_mock.get(
        f'https://api.haskoin.com/btc/address/{btc_test_address}/balance',
        text=haskoin_balance_response,
    )

    api = HaskoinApi()
    balances = api.get_balance(btc_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('0.00064363')


def test_fetch_balances_xpub(requests_mock, haskoin_xpub_response):
    requests_mock.get(
        f'https://api.haskoin.com/btc/xpub/{xpub_test_address}',
        text=haskoin_xpub_response,
    )

    api = HaskoinApi()
    balances = api.get_balance(xpub_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('0.12706308')


def test_fetch_only(requests_mock, haskoin_balance_response):
    requests_mock.get(
        f'https://api.haskoin.com/btc/address/{btc_test_address}/balance',
        text=haskoin_balance_response,
    )

    api = HaskoinApi()
    result = api.fetch_balances(btc_test_address)
    assert result.data['confirmed'] == 64363


def test_parse_address():
    api = HaskoinApi()
    fetch_result = FetchResult(data={'confirmed': 64363})
    result = api.parse_balances(fetch_result)
    assert result.data[0].balance == Decimal('0.00064363')


def test_parse_xpub():
    api = HaskoinApi()
    fetch_result = FetchResult(data={'balance': {'confirmed': 12706308}, 'indices': {}})
    result = api.parse_balances(fetch_result)
    assert result.data[0].balance == Decimal('0.12706308')


def test_fetch_balances_ypub(requests_mock, haskoin_xpub_response):
    converted_xpub = _to_xpub(ypub_test_address)
    requests_mock.get(
        f'https://api.haskoin.com/btc/xpub/{converted_xpub}',
        text=haskoin_xpub_response,
    )

    api = HaskoinApi()
    balances = api.get_balance(ypub_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('0.12706308')

    # Verify derive=compat was passed
    assert requests_mock.last_request.qs['derive'] == ['compat']


def test_fetch_balances_zpub(requests_mock, haskoin_xpub_response):
    converted_xpub = _to_xpub(zpub_test_address)
    requests_mock.get(
        f'https://api.haskoin.com/btc/xpub/{converted_xpub}',
        text=haskoin_xpub_response,
    )

    api = HaskoinApi()
    balances = api.get_balance(zpub_test_address)
    assert len(balances) == 1
    assert balances[0].balance == Decimal('0.12706308')

    # Verify derive=segwit was passed
    assert requests_mock.last_request.qs['derive'] == ['segwit']


def test_to_xpub_roundtrip():
    """ypub/zpub converted to xpub should start with 'xpub' and be valid base58."""
    converted = _to_xpub(ypub_test_address)
    assert converted.startswith('xpub')

    converted = _to_xpub(zpub_test_address)
    assert converted.startswith('xpub')


def test_parse_zero_balance_address():
    api = HaskoinApi()
    fetch_result = FetchResult(data={'confirmed': 0})
    result = api.parse_balances(fetch_result)
    assert result.data is None


def test_parse_zero_balance_xpub():
    api = HaskoinApi()
    fetch_result = FetchResult(data={'balance': {'confirmed': 0}, 'indices': {}})
    result = api.parse_balances(fetch_result)
    assert result.data is None


def test_fetch_invalid_address(requests_mock):
    invalid_address = 'not-a-valid-btc-address'
    requests_mock.get(
        f'https://api.haskoin.com/btc/address/{invalid_address}/balance',
        status_code=400,
        reason='Bad Request',
    )

    api = HaskoinApi()
    result = api.fetch_balances(invalid_address)
    assert result.errors == ['Bad Request']


def test_get_balance_invalid_address_should_raise(requests_mock):
    invalid_address = 'not-a-valid-btc-address'
    requests_mock.get(
        f'https://api.haskoin.com/btc/address/{invalid_address}/balance',
        status_code=400,
        reason='Bad Request',
    )

    api = HaskoinApi()
    with pytest.raises(ApiException, match='Bad Request'):
        api.get_balance(invalid_address)


def test_fetch_error_response(requests_mock):
    requests_mock.get(
        f'https://api.haskoin.com/btc/address/{btc_test_address}/balance',
        status_code=500,
        reason='Internal Server Error',
    )

    api = HaskoinApi()
    result = api.fetch_balances(btc_test_address)
    assert result.errors == ['Internal Server Error']


def test_get_balance_should_raise(requests_mock):
    requests_mock.get(
        f'https://api.haskoin.com/btc/address/{btc_test_address}/balance',
        status_code=500,
        reason='Internal Server Error',
    )

    api = HaskoinApi()
    with pytest.raises(ApiException, match='Internal Server Error'):
        api.get_balance(btc_test_address)


@pytest.fixture
def haskoin_balance_response():
    return read_file('data/haskoin_balance_response.json')


@pytest.fixture
def haskoin_xpub_response():
    return read_file('data/haskoin_xpub_response.json')
