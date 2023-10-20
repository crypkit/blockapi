import datetime
from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.test.v2.api.fake_sleep_provider import FakeSleepProvider
from blockapi.v2.api.nft import OpenSeaApi
from blockapi.v2.base import ApiException
from blockapi.v2.coins import COIN_ETH
from blockapi.v2.models import AssetType, Blockchain, NftOfferDirection

nfts_test_address = '0x539C92186f7C6CC4CbF443F26eF84C595baBBcA1'


@pytest.fixture
def fake_sleep_provider():
    return FakeSleepProvider()


@pytest.fixture
def api(fake_sleep_provider):
    return OpenSeaApi("some-key", Blockchain.ETHEREUM, fake_sleep_provider)


@pytest.fixture
def nfts_response():
    return read_file('data/opensea/nfts.json')


@pytest.fixture
def nfts_next_response():
    return read_file('data/opensea/nfts-next.json')


@pytest.fixture
def offers_response():
    return read_file('data/opensea/offers.json')


@pytest.fixture
def listings_response():
    return read_file('data/opensea/listings.json')


@pytest.fixture
def collection_stats_response():
    return read_file('data/opensea/collection-stats.json')


@pytest.fixture
def collection_response():
    return read_file('data/opensea/collection.json')


def test_fetch_ntfs(
    requests_mock, api, nfts_response, nfts_next_response, fake_sleep_provider
):
    requests_mock.get(
        f'https://api.opensea.io/api/v2/chain/ethereum/account/{nfts_test_address}/nfts',
        text=nfts_response,
    )
    requests_mock.get(
        f'https://api.opensea.io/api/v2/chain/ethereum/account/{nfts_test_address}/nfts?next=LXBrPTE0MDMyMTEyOTU=',
        text=nfts_next_response,
    )

    nfts = api.fetch_nfts(nfts_test_address)
    assert len(nfts.data) == 2
    assert len(fake_sleep_provider.calls)
    assert fake_sleep_provider.calls[0] == ('https://api.opensea.io/', 0.25)


def test_parse_nfts(requests_mock, api, nfts_response, nfts_next_response):
    requests_mock.get(
        f'https://api.opensea.io/api/v2/chain/ethereum/account/{nfts_test_address}/nfts',
        text=nfts_response,
    )
    requests_mock.get(
        f'https://api.opensea.io/api/v2/chain/ethereum/account/{nfts_test_address}/nfts?next=LXBrPTE0MDMyMTEyOTU=',
        text=nfts_next_response,
    )

    nfts = api.fetch_nfts(nfts_test_address)
    parsed = api.parse_nfts(nfts)
    assert len(parsed.data) == 2
    data = parsed.data[1]
    assert data.ident == '550885'
    assert data.collection == 'uniswap-v3-positions'
    assert data.contract == '0xc36442b4a4522e871399cd717abdd847ab11fe88'
    assert data.standard == 'erc721'
    assert data.name == 'Uniswap - 1% - PRIME/WETH - 330.20<>780.29'
    assert (
        data.description
        == 'This NFT represents a liquidity position in a Uniswap V3 PRIME-WETH pool.'
    )
    assert (
        data.image_url
        == 'https://openseauserdata.com/files/8b79194380e9a86f190713e19e78cef8.svg'
    )
    assert (
        data.metadata_url
        == 'data:application/json;base64,eyJuYW1lIjoiVW5pc3dhcCAtIDElIC0gUFJJTUUvV0VUSCAtIDMzMC4yMDw+NzgwLjI5In0='
    )
    assert not data.metadata
    assert data.updated_time == datetime.datetime(2023, 8, 15, 13, 56, 39, 759414)
    assert not data.is_disabled
    assert not data.is_nsfw
    assert data.blockchain == Blockchain.ETHEREUM
    assert data.asset_type == AssetType.AVAILABLE


def test_parse_offers(requests_mock, api, offers_response):
    requests_mock.get(
        f'https://api.opensea.io/api/v2/offers/collection/ever-fragments-of-civitas/all',
        text=offers_response,
    )

    offers = api.fetch_offers('ever-fragments-of-civitas')
    parsed = api.parse_offers(offers)

    assert not parsed.errors
    data = parsed.data[0]

    assert data.direction == NftOfferDirection.OFFER
    assert data.collection == 'ever-fragments-of-civitas'
    assert data.contract == '0x8acb0bc7f6c77e4e2aef83ea928d5a6c2a0b7fcd'
    assert data.start_time == datetime.datetime(
        2023, 10, 5, 1, 50, 13, tzinfo=datetime.timezone.utc
    )
    assert data.end_time == datetime.datetime(
        2023, 10, 11, 1, 50, 13, tzinfo=datetime.timezone.utc
    )

    assert data.offerer == '0xc30992a53b3e91385ace2575963aa392edb3b931'
    assert data.offer_coin.symbol == 'WETH'
    assert not data.offer_ident
    assert data.offer_contract == '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
    assert data.offer_amount == Decimal('0.004')

    assert not data.pay_coin
    assert data.pay_contract == '0x8acb0bc7f6c77e4e2aef83ea928d5a6c2a0b7fcd'
    assert not data.pay_ident
    assert data.pay_amount == Decimal('8')


def test_parse_listings(requests_mock, api, listings_response):
    requests_mock.get(
        f'https://api.opensea.io/api/v2/listings/collection/ever-fragments-of-civitas/all',
        text=listings_response,
    )

    listings = api.fetch_listings('ever-fragments-of-civitas')
    parsed = api.parse_listings(listings)

    assert not parsed.errors
    data = parsed.data[0]

    assert data.direction == NftOfferDirection.LISTING
    assert data.collection == 'ever-fragments-of-civitas'
    assert data.start_time == datetime.datetime(
        2023, 5, 22, 14, 44, 17, tzinfo=datetime.timezone.utc
    )
    assert data.end_time == datetime.datetime(
        2023, 11, 18, 14, 44, 17, tzinfo=datetime.timezone.utc
    )

    assert data.offerer == '0xe4fd714001f6cd80f5ffcfae4d827538d133dfa7'
    assert not data.offer_coin
    assert data.offer_ident == '90000001072'
    assert data.offer_amount == Decimal('1')

    assert data.pay_coin.symbol == 'ETH'
    assert not data.pay_ident
    assert data.pay_amount == Decimal('0.0175')


def test_parse_collection(
    requests_mock, api, collection_response, collection_stats_response
):
    requests_mock.get(
        f'https://api.opensea.io/api/v2/collections/ever-fragments-of-civitas',
        text=collection_response,
    )

    requests_mock.get(
        f'https://api.opensea.io/api/v2/collections/ever-fragments-of-civitas/stats',
        text=collection_stats_response,
    )

    collection = api.fetch_collection('ever-fragments-of-civitas')
    parsed = api.parse_collection(collection)

    assert not parsed.errors
    data = parsed.data[0]
    assert data.name == 'Ever Fragments of Civitas'
    assert data.ident == 'ever-fragments-of-civitas'
    assert (
        data.image
        == 'https://openseauserdata.com/files/f784cefee7f7da9fe4c75ec04279b8b0.png'
    )
    assert not data.is_disabled
    assert not data.is_nsfw
    assert data.total_stats
    assert data.day_stats
    assert not data.week_stats
    assert not data.month_stats

    assert data.total_stats.volume == Decimal('18.813597880000103')
    assert data.total_stats.sales_count == 969
    assert data.total_stats.average_price == Decimal('0.0194154776883386')
    assert data.total_stats.owners_count == 866
    assert data.total_stats.market_cap == Decimal('105.85218269230776')
    assert data.total_stats.floor_price == Decimal('0.008')
    assert data.total_stats.coin == COIN_ETH


def test_create_with_unsupported_blockchain():
    with pytest.raises(ApiException, match="Blockchain 'bitcoin' is not supported"):
        OpenSeaApi('some-key', Blockchain.BITCOIN)
