import pytest
import requests_mock

from blockapi.test.v2.api.conftest import read_json_file
from blockapi.v2.api.sui import SuiApi

TEST_ADDRESS = "0x123"


@pytest.fixture
def sui_response_data():
    return read_json_file('data/sui/response.json')


@pytest.fixture
def mocked_sui_response(requests_mock, sui_response_data):
    requests_mock.post(
        f"https://suiscan.xyz/api/sui-backend/mainnet/api/accounts/0x123/objects",
        status_code=20,
        json=sui_response_data,
    )
    yield requests_mock


def test_sui(mocked_sui_response):
    api = SuiApi()
    balances = api.get_balance(TEST_ADDRESS)
    assert balances

    assert len(balances) == 20
