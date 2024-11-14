import pytest
import requests_mock

from blockapi.test.v2.api.conftest import read_json_file
from blockapi.v2.api.sui import SuiApi

TEST_ADDRESS = "0x123"


@pytest.fixture
def sui_response_data():
    # address 0xc9d60974f954a1492a7a33d86920b348821aad9bf534b845f95e12e01c06a584
    return read_json_file('data/sui/response.json')


@pytest.fixture
def mocked_sui_response(requests_mock, sui_response_data):
    requests_mock.post(
        f"https://api.blockberry.one/sui/v1/accounts/0x123/objects",
        status_code=20,
        json=sui_response_data,
    )
    yield requests_mock


def test_sui(mocked_sui_response):
    api = SuiApi("test_key")
    balances = api.get_balance(TEST_ADDRESS)

    assert balances
    assert len(balances) == 4

    for balance in balances:
        assert balance.coin.address
        assert balance.coin.decimals is not None
        assert balance.coin.symbol
        assert balance.coin.name != 'unknown'

        assert balance
        assert balance.balance_raw
