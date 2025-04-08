import json
from pathlib import Path
from decimal import Decimal

import pytest
import requests_mock

from blockapi.test.v2.api.conftest import read_file
from blockapi.test.v2.api.fake_sleep_provider import FakeSleepProvider
from blockapi.v2.api.nft.unisat import UnisatApi
from blockapi.v2.models import (
    NftToken,
    NftCollection,
    NftOffer,
    NftOfferDirection,
    BtcNftType,
)
from blockapi.v2.models import Blockchain, AssetType

nfts_test_address = 'bc1p3rwga6xsfal6f5d085scecg8lu4gsjl8drk5e07uqzk3cg9dq43s734vje'
test_collection_id = (
    '6fb976ab49dcec017f1e2015b625126c5c4d6b71174f5bc5af4f39b274a4b6b5i0'
)
test_nft_type = BtcNftType.COLLECTION


def test_parse_nfts(requests_mock, unisat_client, inscription_data):
    """Test basic NFT parsing with valid data"""
    requests_mock.get(
        f"{unisat_client.api_options.base_url}v1/indexer/address/{nfts_test_address}/inscription-data",
        text=inscription_data,
    )

    result = unisat_client.fetch_nfts(nfts_test_address)
    assert not result.errors, f"Fetch errors: {result.errors}"

    parsed = unisat_client.parse_nfts(result)
    assert not parsed.errors, f"Parse errors: {parsed.errors}"
    assert len(parsed.data) == 2

    # Test first NFT
    nft1 = parsed.data[0]
    assert (
        nft1.ident
        == "6fb976ab49dcec017f1e2015b625126c5c4d6b71174f5bc5af4f39b274a4b6b5i0"
    )
    assert nft1.collection == "ordinals"
    assert nft1.collection_name == "Bitcoin Ordinals"
    assert (
        nft1.contract
        == "6fb976ab49dcec017f1e2015b625126c5c4d6b71174f5bc5af4f39b274a4b6b5"
    )
    assert nft1.standard == "ordinals"
    assert nft1.name == "Ordinal #12345"
    assert nft1.amount == 1
    assert nft1.updated_time == 1672531200
    assert nft1.blockchain == Blockchain.BITCOIN
    assert nft1.asset_type == AssetType.AVAILABLE

    # Test second NFT
    nft2 = parsed.data[1]
    assert (
        nft2.ident
        == "7fb976ab49dcec017f1e2015b625126c5c4d6b71174f5bc5af4f39b274a4b6b5i0"
    )
    assert nft2.collection == "ordinals"
    assert nft2.collection_name == "Bitcoin Ordinals"
    assert (
        nft2.contract
        == "7fb976ab49dcec017f1e2015b625126c5c4d6b71174f5bc5af4f39b274a4b6b5"
    )
    assert nft2.standard == "ordinals"
    assert nft2.name == "Ordinal #12346"
    assert nft2.amount == 1
    assert nft2.updated_time == 1672531300
    assert nft2.blockchain == Blockchain.BITCOIN
    assert nft2.asset_type == AssetType.AVAILABLE


def test_parse_nfts_edge_cases(
    requests_mock, unisat_client, inscription_data_edge_cases
):
    """Test NFT parsing with various edge cases"""
    requests_mock.get(
        f"{unisat_client.api_options.base_url}v1/indexer/address/{nfts_test_address}/inscription-data",
        text=inscription_data_edge_cases,
    )

    result = unisat_client.fetch_nfts(nfts_test_address)
    assert not result.errors, f"Fetch errors: {result.errors}"

    parsed = unisat_client.parse_nfts(result)
    assert not parsed.errors, f"Parse errors: {parsed.errors}"
    # Should only parse the last inscription as it's the only one with all required fields
    assert len(parsed.data) == 1

    nft = parsed.data[0]
    assert (
        nft.ident
        == "8fb976ab49dcec017f1e2015b625126c5c4d6b71174f5bc5af4f39b274a4b6b5i0"
    )
    assert nft.collection == "ordinals"
    assert nft.collection_name == "Bitcoin Ordinals"
    assert (
        nft.contract
        == "8fb976ab49dcec017f1e2015b625126c5c4d6b71174f5bc5af4f39b274a4b6b5"
    )
    assert nft.standard == "ordinals"
    assert nft.name == "Ordinal #2"
    assert nft.amount == 1
    assert nft.updated_time == 1234567890
    assert nft.blockchain == Blockchain.BITCOIN
    assert nft.asset_type == AssetType.AVAILABLE


def test_fetch_collection(requests_mock, unisat_client, collection_stats):
    requests_mock.post(
        f"{unisat_client.api_options.base_url}v3/market/collection/auction/collection_statistic",
        text=collection_stats,
    )

    test_collection = "pixel-pepes"
    fetch_result = unisat_client.fetch_collection(test_collection)
    assert not fetch_result.errors, f"Fetch errors: {fetch_result.errors}"

    parse_result = unisat_client.parse_collection(fetch_result)
    assert not parse_result.errors, f"Parse errors: {parse_result.errors}"
    assert len(parse_result.data) == 1

    collection = parse_result.data[0]
    assert isinstance(collection, NftCollection)
    assert collection.ident == "pixel-pepes"
    assert collection.name == "Pixel Pepes"
    assert (
        collection.image
        == "https://static.unisat.io/content/47c1d21c508f6d49dfde64d958f14acd041244e1bb616f9b78114b8d9dc7b945i0"
    )
    assert not collection.is_disabled
    assert not collection.is_nsfw
    assert collection.blockchain == Blockchain.BITCOIN
    assert str(collection.total_stats.floor_price) == "990000"
    assert str(collection.total_stats.owners_count) == "1563"
    assert str(collection.total_stats.sales_count) == "20"
    assert str(collection.total_stats.volume) == "39900000"
    assert str(collection.total_stats.market_cap) == str(990000 * 1563)


def test_fetch_listings(requests_mock, unisat_client, listings_data):
    """Test fetching and parsing NFT listings with focus on key attributes"""
    requests_mock.post(
        f"{unisat_client.api_options.base_url}v3/market/collection/auction/list",
        text=listings_data,
    )

    fetch_result = unisat_client.fetch_listings(test_nft_type)
    assert not fetch_result.errors, f"Fetch errors: {fetch_result.errors}"

    parsed = unisat_client.parse_listings(fetch_result)
    assert not parsed.errors, f"Parse errors: {parsed.errors}"
    assert len(parsed.data) == 3

    listing1 = parsed.data[0]
    assert isinstance(listing1, NftOffer)
    assert listing1.offer_key == "ye0io3o6x1wcoc9kbwe1xs5wue5ue4tw"
    assert listing1.direction == NftOfferDirection.LISTING
    assert listing1.collection == "test-collection"
    assert (
        listing1.offerer
        == "bc1prx76vq7rv9cyhn2jrd5ygdsxwznsvpv58ccpfschl9zsp8vh4lws7qenhh"
    )
    assert (
        listing1.offer_ident
        == "3822c34e230b423f7092b4bf96b63cd3377fd02ac40fb025f5153461fe0a4b02i0"
    )
    assert listing1.pay_amount == Decimal('0.0005')  # 50000 satoshis = 0.0005 BTC

    listing2 = parsed.data[1]
    assert listing2.offer_key == "5s7doqj4up5xb2ek5s0rhrwviav2cp0e"
    assert listing2.collection == "test-collection"
    assert (
        listing2.offerer
        == "bc1p7qsamzcjffpvg8ej9dqkf7gp2ygs0xdth3tn4f2a3xvl0jg43f7q25kx3a"
    )
    assert (
        listing2.offer_ident
        == "d5fe1825a1d6240442c67ddf0a312d6b2092a4d526b252935759c236c0bfd057i0"
    )
    assert listing2.pay_amount == Decimal('0.0005')  # 50000 satoshis = 0.0005 BTC

    listing3 = parsed.data[2]
    assert listing3.offer_key == "iegj06ozdwo01swy8u6dvesov7hbp60y"
    assert listing3.collection == "unisat-og-pass"
    assert (
        listing3.offerer
        == "bc1pu7p5nk2ky6gfus5qjt9fguyxq5xsg7ehg4738k3fez07jdv42umqdxj9pr"
    )
    assert (
        listing3.offer_ident
        == "c4d40b8b09a92cc9272cb144c17d128bb0fbb63834c715f2b0a842d2b689cef7i0"
    )
    assert listing3.pay_amount == Decimal('0.5')  # 50000000 satoshis = 0.5 BTC


def test_fetch_offers(requests_mock, unisat_client, offers_data):
    """Test fetching and parsing NFT offers with filtering by Listed status"""
    requests_mock.post(
        f"{unisat_client.api_options.base_url}v3/market/collection/auction/actions",
        text=offers_data,
    )

    fetch_result = unisat_client.fetch_offers(test_nft_type, event="Listed")
    assert not fetch_result.errors, f"Fetch errors: {fetch_result.errors}"

    parsed = unisat_client.parse_offers(fetch_result)
    assert not parsed.errors, f"Parse errors: {parsed.errors}"

    assert len(parsed.data) == 1

    offer = parsed.data[0]
    assert isinstance(offer, NftOffer)
    assert offer.offer_key == "kdw6octea9snqnmoatmxe87uav45a49l"
    assert offer.direction == NftOfferDirection.OFFER
    assert offer.collection == "runestone"
    assert (
        offer.offerer
        == "bc1pme7y9me8z23426xvenrcjcnsdzfw5glu6yewc6vdqxryld8lt6rqzxpu4s"
    )
    assert (
        offer.offer_ident
        == "b37ca7758738d471a22522e2e9de789448991cd854d0020e481037e9df5ff710i1155"
    )
    assert offer.pay_amount == Decimal('0.00174')  # 174000 satoshis = 0.00174 BTC


@pytest.fixture
def fake_sleep_provider():
    return FakeSleepProvider()


@pytest.fixture
def unisat_client(fake_sleep_provider):
    return UnisatApi(api_key="test_key", sleep_provider=fake_sleep_provider)


@pytest.fixture
def inscription_data():
    return read_file('data/unisat/inscription_data.json')


@pytest.fixture
def inscription_data_edge_cases():
    return read_file('data/unisat/inscription_data_edge_cases.json')


@pytest.fixture
def collection_edge_cases():
    return read_file('data/unisat/collection_edge_cases.json')


@pytest.fixture
def listings_data():
    return read_file('data/unisat/listings.json')


@pytest.fixture
def offers_data():
    return read_file('data/unisat/offers.json')


@pytest.fixture
def collection_stats():
    return read_file('data/unisat/collection_stats.json')
