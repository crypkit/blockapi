import datetime
from decimal import Decimal

import pytest
from dateutil.tz import tzutc

from blockapi.test.v2.api.conftest import read_file
from blockapi.test.v2.api.fake_sleep_provider import FakeSleepProvider
from blockapi.v2.api.nft.magic_eden import MagicEdenSolanaApi
from blockapi.v2.coins import COIN_SOL
from blockapi.v2.models import AssetType, Blockchain, FetchResult, NftOfferDirection

nfts_test_address = 'FEeSRuEDk8ENZbpzXjn4uHPz3LQijbeKRzhqVr5zPSJ9'
test_collection_slug = 'magicticket'


def test_parse_nfts(requests_mock, api, nfts_response):
    requests_mock.get(
        f'https://api-mainnet.magiceden.dev/v2/wallets/{nfts_test_address}/tokens',
        text=nfts_response,
    )

    nfts = api.fetch_nfts(nfts_test_address)
    parsed = api.parse_nfts(nfts)

    assert not parsed.cursor

    assert len(parsed.data) == 1
    data = parsed.data[0]
    assert data.ident == 'Hrm8kNwzxikZ9GnpQLLZZanJB8qScxjmKkKbDJ23ZwTb'
    assert data.collection == 'magicticket'
    assert data.contract == 'magicticket'
    assert data.standard == 'erc721'
    assert data.name == 'Magic Ticket: Degen #9753'
    assert data.collection_name == 'Magic Ticket'
    assert not data.description
    assert (
        data.image_url
        == 'https://bafybeigm42xnsdukek7wupydeiu4n7spmqf7zc73r54x3p3jjiw72nlrla.ipfs.dweb.link/0.gif?ext=gif'
    )
    assert not data.metadata_url
    assert not data.metadata
    assert not data.updated_time
    assert not data.is_disabled
    assert not data.is_nsfw
    assert data.blockchain == Blockchain.SOLANA
    assert data.asset_type == AssetType.AVAILABLE
    assert data.amount == 1


def test_parse_collection(requests_mock, api, collection_response):
    requests_mock.get(
        f'https://api-mainnet.magiceden.dev/v2/collections/magicticket/stats',
        text=collection_response,
    )

    collection = api.fetch_collection(test_collection_slug)
    parsed = api.parse_collection(fetch_result=collection)

    assert not parsed.errors
    data = parsed.data[0]
    assert data.name == 'magicticket'
    assert data.ident == 'magicticket'
    assert not data.image
    assert not data.is_disabled
    assert not data.is_nsfw
    assert data.total_stats
    assert not data.day_stats
    assert not data.week_stats
    assert not data.month_stats

    assert data.total_stats.volume == Decimal('277115.43619589294')
    assert data.total_stats.average_price == Decimal('2.9260941626261516')
    assert data.total_stats.floor_price == Decimal('2.69')
    assert data.total_stats.coin == COIN_SOL
    assert data.blockchain == Blockchain.SOLANA
    assert len(data.contracts) == 1
    assert data.contracts[0].blockchain == Blockchain.SOLANA
    assert data.contracts[0].address == 'magicticket'


def test_parse_offers(requests_mock, api, offers_response):
    requests_mock.get(
        f'https://api-mainnet.magiceden.dev/v2/mmm/pools?collectionSymbol=mad_lads&showInvalid=false&offset=0&limit=500&filterOnSide=0&hideExpired=true&direction=1&field=5&attributesMode=0&attributes=%5B%5D&enableSNS=true',
        text=offers_response,
    )

    offers = api.fetch_offers('mad_lads')
    parsed = api.parse_offers(fetch_result=offers)

    assert not parsed.errors
    assert not parsed.cursor

    data = parsed.data[0]

    assert data.direction == NftOfferDirection.OFFER
    assert data.offer_key == 'Gk3MRAdWDNu3SdUYRLWyBeQ7tua1zDBPxAyk858XUDSZ'
    assert data.blockchain == Blockchain.SOLANA
    assert data.collection == 'mad_lads'
    assert data.contract == 'mad_lads'
    assert data.start_time == datetime.datetime(
        2024, 2, 14, 4, 56, 56, 763000, tzinfo=tzutc()
    )
    assert data.end_time is None
    assert data.offerer == 'AbwGJTBZxACtJ62cTAWxaQZFsVBB3BDLVzon7nA6b8YS'
    assert data.offer_coin.symbol == 'SOL'
    assert not data.offer_ident
    assert not data.offer_contract
    assert data.offer_amount == Decimal('144.66873231')

    assert not data.pay_coin
    assert data.pay_contract == 'mad_lads'
    assert not data.pay_ident
    assert data.pay_amount == Decimal('1')


def test_parse_listings(requests_mock, api, listings_response):
    requests_mock.get(
        f'https://api-mainnet.magiceden.dev/v2/collections/magicticket/listings?offset=0&limit=100',
        text=listings_response,
    )

    listings = api.fetch_listings(test_collection_slug)
    assert not listings.errors
    parsed = api.parse_listings(fetch_result=listings)

    assert not parsed.errors
    data = parsed.data[0]

    assert data.direction == NftOfferDirection.LISTING
    assert (
        data.offer_key
        == 'magicticket_2fJjmyyzKJSac9B4AgLuHUieg61SifcV4iX2Ss4tqbZa_2jwVXX5FFFpcFgLAk82XyKUYtk9k5gJAxN1p1z5upxmK'
    )
    assert data.blockchain == Blockchain.SOLANA
    assert data.collection == 'magicticket'
    assert data.start_time == datetime.datetime(
        1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
    )
    assert not data.end_time

    assert data.offerer == '2jwVXX5FFFpcFgLAk82XyKUYtk9k5gJAxN1p1z5upxmK'
    assert not data.offer_coin
    assert data.offer_ident == '2fJjmyyzKJSac9B4AgLuHUieg61SifcV4iX2Ss4tqbZa'
    assert data.offer_amount == Decimal('1')

    assert data.pay_coin.symbol == 'SOL'
    assert not data.pay_ident
    assert data.pay_amount == Decimal('2.588235261')


def test_retry_condition(api):
    assert api._should_retry(FetchResult(errors=['Service unavailable']))
    assert api._should_retry(FetchResult(errors=['Service Unavailable']))
    assert not api._should_retry(FetchResult(errors=['Other error']))
    assert not api._should_retry(FetchResult(errors=[dict(message='Composed error')]))


@pytest.fixture
def fake_sleep_provider():
    return FakeSleepProvider()


@pytest.fixture
def api(fake_sleep_provider):
    return MagicEdenSolanaApi(fake_sleep_provider)


@pytest.fixture
def nfts_response():
    return read_file('data/magiceden/wallet-response.json')


@pytest.fixture
def collection_response():
    return read_file('data/magiceden/collection-stats.json')


@pytest.fixture
def listings_response():
    return read_file('data/magiceden/listings.json')


@pytest.fixture
def offers_response():
    return read_file('data/magiceden/offers.json')
