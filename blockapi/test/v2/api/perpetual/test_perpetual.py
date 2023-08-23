import os

import pytest
from _decimal import Decimal

from blockapi.v2.api import PerpetualApi, perp_contract_address
from blockapi.v2.base import ApiException
from blockapi.v2.models import FetchResult


@pytest.fixture
def perp_api():
    return PerpetualApi('http://localhost:2048/')


test_address = '0x134089B387E22f52b1e06CC80d9a5F622032EF74'


def test_perp_contract_address():
    contract = perp_contract_address('PERP')
    assert contract == '0xbC396689893D065F41bc2C6EcbeE5e0085233447'


def test_perp_invalid_contract_raises():
    with pytest.raises(ValueError, match='Invalid contract name.'):
        perp_contract_address("abc")


def test_perp_has_coin(perp_api):
    assert perp_api.coin.symbol == 'PERP'


def filter_infura_key(request):
    if 'infura.io' in request.host:
        request.uri = 'https://mainnet.infura.io/v3/API_KEY_FILTERED'
    return request


@pytest.mark.integration
def test_fetch():
    key = os.environ.get('INFURA_API_KEY')
    api = PerpetualApi(f'https://mainnet.infura.io/v3/{key}')
    raw = api.fetch_balances(test_address)
    assert raw.data


@pytest.mark.integration
def test_fetch_error():
    api = PerpetualApi(f'https://mainnet.infura.io/v3/no-key')
    raw = api.fetch_balances(test_address)
    assert raw.status_code == 401
    assert (
        raw.errors[0]
        == '401 Client Error: Unauthorized for url: https://mainnet.infura.io/v3/no-key'
    )


def test_fetch_error_raises_from_get_balances():
    api = PerpetualApi(f'https://mainnet.infura.io/v3/no-key')
    with pytest.raises(ApiException) as exc:
        api.get_balance(test_address)

    assert exc.match('401 Client Error: Unauthorized for url')


def test_parse(perp_api):
    raw = FetchResult(
        status_code=200,
        data=dict(
            staking_claimable='1.10',
            vesting_claimable='2.02',
            vesting_locked='3.30',
        ),
    )

    parsed = perp_api.parse_balances(raw)

    assert parsed.data[0].balance == Decimal('3.12')
    assert parsed.data[1].balance == Decimal('3.30')
