import logging
from typing import Optional, Dict, Generator
from datetime import datetime

from blockapi.v2.base import BlockchainApi, INftParser, INftProvider, ISleepProvider
from blockapi.v2.coins import COIN_BTC
from blockapi.v2.models import (
    ApiOptions,
    AssetType,
    Blockchain,
    Coin,
    ContractInfo,
    FetchResult,
    NftToken,
    ParseResult,
    NftCollection,
    NftCollectionTotalStats,
    NftVolumes,
)
from requests import HTTPError
import requests

logger = logging.getLogger(__name__)


class UnisatApi(BlockchainApi, INftParser, INftProvider):
    """
    API docs: https://docs.unisat.io/
    """

    coin = COIN_BTC

    api_options = ApiOptions(
        blockchain=Blockchain.BITCOIN,
        base_url='https://open-api.unisat.io/v1/indexer/',
        rate_limit=0.2,  # 5 calls per second for free tier
    )

    supported_requests = {
        'get_nfts': 'address/{address}/inscription-data',
        'get_collection': 'collection-indexer/collection/{collectionId}/info',
        'get_collection_items': 'collection-indexer/collection/{collectionId}/items',
        'get_collection_stats': 'v3/market/collection/auction/collection_statistic',
    }

    def __init__(self, api_key: str, sleep_provider: Optional[ISleepProvider] = None):
        """
        Initialize the Unisat API client

        Args:
            api_key: Your Unisat API key. Required for all API calls.
            sleep_provider: Optional sleep provider for rate limiting
        """
        if not api_key:
            raise ValueError("API key is required for Unisat API")

        super().__init__(sleep_provider=sleep_provider)
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }

    def fetch_nfts(
        self, address: str, cursor: Optional[int] = None, size: int = 16
    ) -> FetchResult:
        """
        Fetch NFTs (inscriptions) owned by the address

        Args:
            address: BTC address to fetch NFTs for
            cursor: Pagination cursor (offset)
            size: Number of items to return per page (default: 16)

        Returns:
            FetchResult containing the NFT data

        Raises:
            ValueError: If address is empty or invalid
        """
        if not address:
            raise ValueError("Address is required")

        params = {'size': size}
        if cursor is not None:
            params['cursor'] = cursor

        try:
            return self.get_data(
                'get_nfts',
                headers=self.headers,
                params=params,
                address=address,
                extra=dict(address=address),
            )
        except (HTTPError, ValueError, TypeError) as e:
            logger.error(f"Error fetching NFTs for address {address}: {str(e)}")
            return FetchResult(errors=[str(e)])
        except Exception as e:
            logger.error(
                f"Unexpected error fetching NFTs for address {address}: {str(e)}"
            )
            return FetchResult(errors=[str(e)])

    def parse_nfts(self, fetch_result: FetchResult) -> ParseResult:
        """Parse NFT data from API response"""
        errors = []
        data = []
        cursor = None

        try:
            if not fetch_result.data:
                errors.append("No data in fetch result")
                return ParseResult(data=[], errors=errors)

            inner_data = fetch_result.data.get("data", {})
            if not inner_data:
                errors.append("No data in API response")
                return ParseResult(data=[], errors=errors)

            cursor = (
                str(inner_data.get("cursor"))
                if inner_data.get("cursor") is not None
                else None
            )

            for nft in self._yield_parsed_nfts(inner_data):
                data.append(nft)

            return ParseResult(data=data, errors=errors, cursor=cursor)

        except Exception as e:
            errors.append(str(e))
            logger.error(f"Error parsing NFTs: {e}")
            return ParseResult(data=[], errors=errors)

    def _yield_parsed_nfts(self, data: Dict) -> Generator[NftToken, None, None]:
        """Yield parsed NFT tokens from API response data"""
        if not data or "inscription" not in data:
            return

        for item in data["inscription"]:
            try:
                if not all(
                    k in item
                    for k in [
                        "inscriptionId",
                        "inscriptionNumber",
                        "timestamp",
                        "utxo",
                    ]
                ):
                    logger.warning(f"Missing required fields in NFT data: {item}")
                    continue

                utxo = item["utxo"]
                if not all(k in utxo for k in ["txid", "address"]):
                    logger.warning(f"Missing required fields in UTXO data: {utxo}")
                    continue

                inscription_number = str(item["inscriptionNumber"])
                timestamp = str(item["timestamp"])

                yield NftToken(
                    ident=item["inscriptionId"],
                    collection="ordinals",
                    collection_name="Bitcoin Ordinals",
                    contract=utxo["txid"],
                    standard="ordinals",
                    name=f"Ordinal #{inscription_number}",
                    description="",
                    amount=1,
                    image_url="",
                    metadata_url=None,
                    metadata={},
                    updated_time=int(timestamp),
                    is_disabled=False,
                    is_nsfw=False,
                    blockchain=Blockchain.BITCOIN,
                    asset_type=AssetType.AVAILABLE,
                    market_url=None,
                )
            except Exception as e:
                logger.warning(f"Error parsing NFT item {item}: {e}")
                continue

    def fetch_collection(self, collection: str) -> FetchResult:
        """Fetch collection data from Unisat API."""
        info_response = self.get_data(
            'get_collection_info',
            headers=self.headers,
            params={'collectionId': collection},
        )
        items_response = self.get_data(
            'get_collection_items',
            headers=self.headers,
            params={'collectionId': collection},
        )
        stats_response = self.get_data(
            'get_collection_stats',
            method='post',
            headers=self.headers,
            json={'collectionId': collection},
        )

        return FetchResult.from_fetch_results([info_response, items_response, stats_response])

    def parse_collection(self, fetch_result: FetchResult) -> ParseResult:
        """
        Parse collection data from the API response

        Args:
            fetch_result: Raw API response data

        Returns:
            ParseResult containing parsed collection data
        """
        if not fetch_result or not fetch_result.data:
            return ParseResult(errors=fetch_result.errors if fetch_result else None)

        try:
            info = fetch_result.data.get('info', {}).get('data', {})
            items = fetch_result.data.get('items', {}).get('data', {})
            stats = fetch_result.data.get('stats', {}).get('data', {})

            total_stats = NftCollectionTotalStats.from_api(
                volume='',
                sales_count='',
                owners_count=str(info.get('holders', '')),
                market_cap='',
                floor_price=str(stats.get('floorPrice', '')),
                average_price='',
                coin=self.coin,
            )

            collection = NftCollection.from_api(
                ident=collection,
                name=stats.get('name', f"Collection {collection}"),
                contracts=[
                    ContractInfo.from_api(
                        blockchain=Blockchain.BITCOIN, address=collection
                    )
                ],
                image=stats.get('icon'),
                is_disabled=False,
                is_nsfw=False,
                blockchain=Blockchain.BITCOIN,
                total_stats=total_stats,
                volumes=NftVolumes.from_api(
                    coin=self.coin,
                ),
            )

            return ParseResult(
                data=[collection] if collection else [],
                errors=fetch_result.errors,
            )
        except (ValueError, TypeError, AttributeError) as e:
            logger.error(f"Error parsing collection data: {str(e)}")
            return ParseResult(errors=[str(e)])
        except Exception as e:
            logger.error(f"Unexpected error parsing collection data: {str(e)}")
            return ParseResult(errors=[str(e)])

    # Empty implementations for required interface methods
    def fetch_offers(self, collection: str) -> FetchResult:
        """Not implemented yet"""
        return FetchResult()

    def parse_offers(self, fetch_result: FetchResult) -> ParseResult:
        """Not implemented yet"""
        return ParseResult()

    def fetch_listings(self, collection: str) -> FetchResult:
        """Not implemented yet"""
        return FetchResult()

    def parse_listings(self, fetch_result: FetchResult) -> ParseResult:
        """Not implemented yet"""
        return ParseResult()
