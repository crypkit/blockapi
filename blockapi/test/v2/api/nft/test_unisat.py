import json
from pathlib import Path

import pytest
import requests_mock

from blockapi.test.v2.api.conftest import read_file
from blockapi.test.v2.api.fake_sleep_provider import FakeSleepProvider
from blockapi.v2.api.nft.unisat import UnisatApi
from blockapi.v2.models import NftToken, NftCollection
from blockapi.v2.models import Blockchain, AssetType

nfts_test_address = 'bc1p3rwga6xsfal6f5d085scecg8lu4gsjl8drk5e07uqzk3cg9dq43s734vje'
test_collection_id = (
    '6fb976ab49dcec017f1e2015b625126c5c4d6b71174f5bc5af4f39b274a4b6b5i0'
)


def test_parse_nfts(requests_mock, unisat_client, inscription_data):
    """Test basic NFT parsing with valid data"""
    requests_mock.get(
        f"{unisat_client.api_options.base_url}address/{nfts_test_address}/inscription-data",
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
        f"{unisat_client.api_options.base_url}address/{nfts_test_address}/inscription-data",
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


def test_fetch_collection(
    requests_mock, unisat_client, collection_info, collection_items, collection_stats
):
    requests_mock.get(
        f"{unisat_client.api_options.base_url}collection-indexer/collection/{test_collection_id}/info",
        text=collection_info,
    )
    requests_mock.get(
        f"{unisat_client.api_options.base_url}collection-indexer/collection/{test_collection_id}/items",
        text=collection_items,
    )
    requests_mock.post(
        f"{unisat_client.api_options.base_url}v3/market/collection/auction/collection_statistic",
        text=collection_stats,
    )

    fetch_result = unisat_client.fetch_collection(test_collection_id)
    assert not fetch_result.errors, f"Fetch errors: {fetch_result.errors}"

    parse_result = unisat_client.parse_collection(fetch_result)
    assert not parse_result.errors, f"Parse errors: {parse_result.errors}"
    assert len(parse_result.data) == 1

    collection = parse_result.data[0]
    assert isinstance(collection, NftCollection)
    assert collection.ident == test_collection_id
    assert collection.name == "Ordinal Punks"
    assert (
        collection.image
        == "https://ordinals.com/content/6fb976ab49dcec017f1e2015b625126c5c4d6b71174f5bc5af4f39b274a4b6b5i0"
    )
    assert not collection.is_disabled
    assert not collection.is_nsfw
    assert str(collection.total_stats.owners_count) == "150"
    assert str(collection.total_stats.floor_price) == "0.1"


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
def collection_info():
    return read_file('data/unisat/collection_info.json')


@pytest.fixture
def collection_items():
    return read_file('data/unisat/collection_items.json')


@pytest.fixture
def collection_stats():
    return read_file('data/unisat/collection_stats.json')


@pytest.fixture
def inscription_data_edge_cases():
    return read_file('data/unisat/inscription_data_edge_cases.json')


@pytest.fixture
def collection_edge_cases():
    return read_file('data/unisat/collection_edge_cases.json')
