import datetime
from decimal import Decimal

import pytest
from dateutil.tz import tzutc

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api.nft import SimpleHashApi
from blockapi.v2.coins import COIN_BTC
from blockapi.v2.models import AssetType, Blockchain, FetchResult, NftOfferDirection

nfts_test_address = 'bc1p3rwga6xsfal6f5d085scecg8lu4gsjl8drk5e07uqzk3cg9dq43s734vje'
test_collection_slug = '4d5b1ef2d87f2212c7b00300296439da'


def test_parse_nfts(requests_mock, api, nfts_response):
    requests_mock.get(
        f'https://api.simplehash.com/api/v0/nfts/owners?chains=bitcoin&wallet_addresses={nfts_test_address}',
        text=nfts_response,
    )

    nfts = api.fetch_nfts(nfts_test_address)
    parsed = api.parse_nfts(nfts)

    assert not nfts.errors
    assert parsed.cursor == (
        'YnRjLW0uODc5MGYyYmMyZmU0YmQ5ZWNmZGIxMzVmNmEwYzFjZmZkYzRiY2RhZGMzN'
        'jE2MjYxZjcwNDQwNGViMmY2NzVlNmkwLjAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMD'
        'AwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA'
        'wMDAwMF8yMDIzLTA1LTI2IDE3OjE0OjQ5KzAwOjAwX19uZXh0'
    )

    assert len(parsed.data) == 1
    data = parsed.data[0]
    assert (
        data.ident
        == 'bitcoin.0477f95b55d8770363e3b7beb6f0320dad38f2915d2fdf99c4271ae1bc266dc2i0'
    )
    assert data.collection == '4d5b1ef2d87f2212c7b00300296439da'
    assert data.contract == '4d5b1ef2d87f2212c7b00300296439da'
    assert data.standard == 'ordinals'
    assert data.name == 'Bitcoin Frog #7825'
    assert not data.collection_name
    assert not data.description
    assert (
        data.image_url
        == 'https://cdn.simplehash.com/assets/4c2181b3f92d934a3d894f02b1e6bd3c22259ae35e90138cacf8a55b06851050.webp'
    )
    assert not data.metadata_url
    assert not data.metadata
    assert data.updated_time == datetime.datetime(2023, 3, 11, 3, 46, 15)
    assert not data.is_disabled
    assert not data.is_nsfw
    assert data.blockchain == Blockchain.BITCOIN
    assert data.asset_type == AssetType.AVAILABLE
    assert data.amount == 1


def test_parse_collection(requests_mock, api, collection_response):
    requests_mock.get(
        f'https://api.simplehash.com/api/v0/nfts/collections/ids?collection_ids={test_collection_slug}',
        text=collection_response,
    )

    collection = api.fetch_collection(test_collection_slug)
    parsed = api.parse_collection(fetch_result=collection)

    assert not parsed.errors
    data = parsed.data[0]
    assert data.name == 'Bitcoin Frogs'
    assert data.ident == '4d5b1ef2d87f2212c7b00300296439da'
    assert data.image == (
        'https://lh3.googleusercontent.com/2potrs-yhEC3T7JvVVS0oGUp6ekCurbV5J4eFgTWbXsZj6L'
        '-L3nDlxVRm_VVhq5UihEYoYQumRK-907MkISJP8ddPAgTpEOCiHE'
    )
    assert not data.is_disabled
    assert not data.is_nsfw
    assert data.total_stats
    assert not data.day_stats
    assert not data.week_stats
    assert not data.month_stats

    assert data.total_stats.volume == Decimal('0')
    assert data.total_stats.average_price == Decimal('0')
    assert data.total_stats.floor_price == Decimal('0.15499')
    assert data.total_stats.coin == COIN_BTC
    assert data.blockchain == Blockchain.BITCOIN
    assert len(data.contracts) == 1
    assert data.contracts[0].blockchain == Blockchain.BITCOIN
    assert data.contracts[0].address == '4d5b1ef2d87f2212c7b00300296439da'


def test_inscriptions_collection(requests_mock, api, collection_response):
    requests_mock.get(
        f'https://api.simplehash.com/api/v0/nfts/collections/ids?collection_ids=inscriptions',
        text='',
    )

    collection = api.fetch_collection('inscriptions')
    parsed = api.parse_collection(fetch_result=collection)

    assert not parsed.errors
    data = parsed.data[0]
    assert data.name == 'Inscriptions'
    assert data.ident == 'inscriptions'
    assert not data.image
    assert not data.is_disabled
    assert not data.is_nsfw
    assert data.total_stats
    assert not data.day_stats
    assert not data.week_stats
    assert not data.month_stats

    assert data.total_stats.volume == Decimal('0')
    assert data.total_stats.average_price == Decimal('0')
    assert data.total_stats.floor_price == Decimal('0')
    assert data.total_stats.coin == COIN_BTC
    assert data.blockchain == Blockchain.BITCOIN
    assert len(data.contracts) == 1
    assert data.contracts[0].blockchain == Blockchain.BITCOIN
    assert data.contracts[0].address == 'inscriptions'


def test_parse_offers(requests_mock, api, offers_response):
    requests_mock.get(
        f'https://api.simplehash.com/api/v0/nfts/bids/collection/{test_collection_slug}',
        text=offers_response,
    )

    offers = api.fetch_offers(test_collection_slug)
    parsed = api.parse_offers(fetch_result=offers)

    assert not parsed.errors
    assert parsed.cursor == (
        'MjAyNC0wMi0yMCAwMTozOToyOS0wODJlZTNlZDY1YzY1ODc4ZTc'
        '4ZTgwMjI4NzAyNjM1NGFjX29wZW5zZWFfMHgxMzgwY2U2NjUxMj'
        'Y0ODk4NjUwZDRhZDE4NDkwMDA1MjA3YjQ2MzUwNDMzOGYyYzk2N'
        'TBmOTBmZDFjNzhhZGFmX19uZXh0'
    )

    data = parsed.data[0]

    assert data.direction == NftOfferDirection.OFFER
    assert data.offer_key == '0d243797b0b1186dfedb3b8a58556d0f'
    assert data.blockchain == Blockchain.BITCOIN
    assert data.collection == '4d5b1ef2d87f2212c7b00300296439da'
    assert data.contract == '4d5b1ef2d87f2212c7b00300296439da'
    assert data.start_time == datetime.datetime(2024, 2, 20, 9, 42, 55, tzinfo=tzutc())
    assert data.end_time == datetime.datetime(2024, 2, 20, 9, 57, 55, tzinfo=tzutc())
    assert (
        data.offerer == 'bc1paw8hlk6aucjv9pluj5fdhtzlvg7qyeg2y8f6thw5vpxe8cf3kh4scyz2d2'
    )
    assert data.offer_coin.symbol == 'BTC'
    assert not data.offer_ident
    assert not data.offer_contract
    assert data.offer_amount == Decimal('1.485')

    assert not data.pay_coin
    assert data.pay_contract == '4d5b1ef2d87f2212c7b00300296439da'
    assert (
        data.pay_ident
        == 'bitcoin.0477f95b55d8770363e3b7beb6f0320dad38f2915d2fdf99c4271ae1bc266dc2i0'
    )
    assert data.pay_amount == Decimal('1')


def test_parse_listings(requests_mock, api, listings_response):
    requests_mock.get(
        f'https://api.simplehash.com/api/v0/nfts/listings/collection/{test_collection_slug}',
        text=listings_response,
    )

    listings = api.fetch_listings(test_collection_slug)
    assert not listings.errors
    parsed = api.parse_listings(fetch_result=listings)

    assert not parsed.errors
    data = parsed.data[0]

    assert data.direction == NftOfferDirection.LISTING
    assert data.offer_key == 'b224b405af11958569f94a44f24cfbaf'
    assert data.blockchain == Blockchain.BITCOIN
    assert data.collection == '4d5b1ef2d87f2212c7b00300296439da'
    assert data.start_time == datetime.datetime(
        2024, 2, 20, 8, 52, 53, 871000, tzinfo=tzutc()
    )
    assert not data.end_time

    assert (
        data.offerer == 'bc1paw8hlk6aucjv9pluj5fdhtzlvg7qyeg2y8f6thw5vpxe8cf3kh4scyz2d2'
    )
    assert not data.offer_coin
    assert (
        data.offer_ident
        == 'bitcoin.0477f95b55d8770363e3b7beb6f0320dad38f2915d2fdf99c4271ae1bc266dc2i0'
    )
    assert data.offer_amount == Decimal('1')

    assert data.pay_coin.symbol == 'BTC'
    assert not data.pay_ident
    assert data.pay_amount == Decimal('1.485')


@pytest.fixture
def api():
    return SimpleHashApi('fake_key')


@pytest.fixture
def nfts_response():
    return read_file('data/simplehash/nfts.json')


@pytest.fixture
def collection_response():
    return read_file('data/simplehash/collection.json')


@pytest.fixture
def listings_response():
    return read_file('data/simplehash/listings.json')


@pytest.fixture
def offers_response():
    return read_file('data/simplehash/offers.json')
