import os

import pytest

from blockapi.v2.api.perpetual import PerpetualApi, perp_contract_address


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
@pytest.mark.vcr(before_record_request=filter_infura_key)
def test_perp_get_balances():
    key = os.environ.get('INFURA_API_KEY')
    perp_api = PerpetualApi(f'https://mainnet.infura.io/v3/{key}')
    balances = perp_api.get_balance(test_address)
    assert balances[0].balance
    assert balances[1].balance
