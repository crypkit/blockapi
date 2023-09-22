import json
from typing import Optional

import pytest

from blockapi.v2.api.nft import InfuraNftApi
from blockapi.v2.api.nft.infura import InfuraNftAssetsResponse

TEST_ADDRESS = '0x0a267cf51ef038fc00e71801f5a524aec06e4f07'
TEST_CURSOR = 'eyJhbGciOiJIUzI1NiJ9'


@pytest.fixture
def infura_nft_api():
    return InfuraNftApi('some-api-key')


@pytest.fixture
def infura_empty_nft_data() -> dict:
    return dict(
        total=0,
        pageNumber=1,
        pageSize=100,
        network='ETHEREUM',
        account='0x0a267cf51ef038fc00e71801f5a524aec06e4f07',
        cursor=None,
        assets=[],
    )


@pytest.fixture
def infura_first_page_nft_data() -> dict:
    return dict(
        total=2,
        pageNumber=1,
        pageSize=1,
        network='ETHEREUM',
        account='0x0a267cf51ef038fc00e71801f5a524aec06e4f07',
        cursor=TEST_CURSOR,
        assets=[
            dict(
                contract='0x76be3b62873462d2142405439777e971754e8e77',
                tokenId='10320',
                supply="4",
                type="ERC1155",
                metadata=dict(
                    name='Cleanse the Earth',
                    description=(
                        "We humans can sometimes forget the damage we do to the earth and that the only way "
                        "to fix it is to wipe the slate clean. Looks like its time for a reminder."
                    ),
                    image='https://nftmedia.parallelnft.com/parallel-alpha/some-hash/image.png',
                    external_url='https://rarible.com/token/0x76be3b62873462d2142405439777e971754e8e77:10320',
                    attributes=[
                        dict(key="Artist", trait_type="Artist", value='Oscar Mar')
                    ],
                    token_id=10320,
                ),
            )
        ],
    )


@pytest.fixture
def infura_second_page_nft_data() -> dict:
    return dict(
        total=2,
        pageNumber=2,
        pageSize=1,
        network='ETHEREUM',
        account='0x0a267cf51ef038fc00e71801f5a524aec06e4f07',
        cursor=None,
        assets=[
            dict(
                contract='0x0fc3dd8c37880a297166bed57759974a157f0e74',
                tokenId='2565',
                supply="1",
                type="ERC721",
                metadata=dict(
                    name='Unrevealed Avatar',
                    description="You can reveal the Parallel of this Avatar at https://parallel.life/avatars",
                    image='https://nftmedia.parallelnft.com/parallel-alpha/some-hash/image.png',
                    external_url="https://parallel.life/avatars/nfts/2565",
                    attributes=[
                        dict(key="Parallel", trait_type="Parallel", value='Unrevealed')
                    ],
                    token_id=2565,
                ),
            )
        ],
    )


def _mock_response_data(requests_mock, data, cursor: Optional[str] = None):
    url = f'https://nft.api.infura.io/networks/1/accounts/{TEST_ADDRESS}/assets/nfts'
    if cursor:
        url += '?cursor=' + cursor

    requests_mock.get(url, text=json.dumps(data))


def test_fetch_empty_set(requests_mock, infura_nft_api, infura_empty_nft_data):
    _mock_response_data(requests_mock, infura_empty_nft_data)
    fetch_data = infura_nft_api.fetch_nft(TEST_ADDRESS)
    assert fetch_data.data == [infura_empty_nft_data]


def test_verify_asset_data(requests_mock, infura_nft_api, infura_second_page_nft_data):
    _mock_response_data(requests_mock, infura_second_page_nft_data)
    fetch_data = infura_nft_api.fetch_nft(TEST_ADDRESS)
    assert fetch_data.data == [infura_second_page_nft_data]


def test_use_cursor_to_fetch_multiple_times(
    requests_mock,
    infura_nft_api,
    infura_first_page_nft_data,
    infura_second_page_nft_data,
):
    _mock_response_data(requests_mock, infura_first_page_nft_data)
    _mock_response_data(requests_mock, infura_second_page_nft_data, cursor=TEST_CURSOR)
    fetch_data = infura_nft_api.fetch_nft(TEST_ADDRESS)
    items = fetch_data.data
    assert items == [infura_first_page_nft_data, infura_second_page_nft_data]


def test_request_contains_correct_headers(
    requests_mock, infura_nft_api, infura_empty_nft_data
):
    _mock_response_data(requests_mock, infura_empty_nft_data)
    infura_nft_api.fetch_nft(TEST_ADDRESS)
    assert requests_mock.last_request.headers['accept'] == 'application/json'
    assert requests_mock.last_request.headers['authorization'] == 'Basic some-api-key'


def test_parse_balances(
    infura_nft_api, infura_first_page_nft_data, infura_second_page_nft_data
):
    items = infura_nft_api.parse_nft(
        dict(items=[infura_first_page_nft_data, infura_second_page_nft_data])
    )
    balances = items['balances']
    assert len(balances) == 2
    assert balances[0].balance == 4
    assert balances[0].name
    assert balances[0].description
