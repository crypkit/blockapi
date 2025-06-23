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


def test_fetch_collection_icon_code(requests_mock, unisat_client, collection_stats):
    """
    UniSat sometimes sends only the icon *code* ― no URL.
    We expect `parse_collection` to prepend the static CDN prefix automatically.
    """
    requests_mock.post(
        f"{unisat_client.api_options.base_url}"
        "v3/market/collection/auction/collection_statistic",
        text=collection_stats,
    )

    fetch_result = unisat_client.fetch_collection("pixel-pepes")
    assert not fetch_result.errors

    parsed = unisat_client.parse_collection(fetch_result)
    assert not parsed.errors and len(parsed.data) == 1

    col: NftCollection = parsed.data[0]
    assert col.ident == "pixel-pepes"
    assert col.name == "Pixel Pepes"
    assert (
        col.image == "https://static.unisat.io/content/"
        "47c1d21c508f6d49dfde64d958f14acd041244e1bb616f9b78114b8d9dc7b945i0"
    )
    assert str(col.total_stats.floor_price) == "0.0099"
    assert str(col.total_stats.volume) == "0.399"


def test_fetch_collection_icon_full_url(
    requests_mock, unisat_client, collection_stats_full_url
):
    """
    UniSat may also deliver a *fully-qualified* icon URL.
    In that case we should **not** touch the value.
    """
    requests_mock.post(
        f"{unisat_client.api_options.base_url}"
        "v3/market/collection/auction/collection_statistic",
        text=collection_stats_full_url,
    )

    fetch_result = unisat_client.fetch_collection("rune-mania-miner")
    assert not fetch_result.errors

    parsed = unisat_client.parse_collection(fetch_result)
    assert not parsed.errors and len(parsed.data) == 1

    col: NftCollection = parsed.data[0]
    assert col.ident == "rune-mania-miner"
    assert col.name == "Rune Mania Miner"
    assert (
        col.image == "https://creator-hub-prod.s3.us-east-2.amazonaws.com/"
        "ord-rmm_pfp_1708461604099.png"
    )

    assert str(col.total_stats.floor_price) == "0.0008"


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
def listings_data():
    return read_file('data/unisat/listings.json')


@pytest.fixture
def offers_data():
    return read_file('data/unisat/offers.json')


@pytest.fixture
def collection_stats():
    """Pixel Pepes – icon **code** only."""
    return read_file("data/unisat/collection_stats.json")


@pytest.fixture
def collection_stats_full_url():
    """Rune Mania Miner – icon is a full URL."""
    return read_file("data/unisat/collection_stats_full_url.json")
