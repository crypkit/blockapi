import logging
from typing import Optional

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
        if not fetch_result or not fetch_result.data:
            return ParseResult(errors=fetch_result.errors if fetch_result else None)

        try:
            parsed = list(self._yield_parsed_nfts(fetch_result.data))
            return ParseResult(
                data=parsed,
                errors=fetch_result.errors,
                cursor=fetch_result.data.get('cursor'),
            )
        except (ValueError, TypeError, AttributeError) as e:
            logger.error(f"Error parsing NFT data: {str(e)}")
            return ParseResult(errors=[str(e)])
        except Exception as e:
            logger.error(f"Unexpected error parsing NFT data: {str(e)}")
            return ParseResult(errors=[str(e)])

    def _yield_parsed_nfts(self, data: dict):
        inscriptions = data.get('inscription', [])

        if not inscriptions:
            return

        for inscription in inscriptions:
            inscription_id = inscription.get('inscriptionId')
            inscription_number = inscription.get('inscriptionNumber')
            utxo = inscription.get('utxo', {})
            txid = utxo.get('txid')

            if not all([inscription_id, inscription_number, txid]):
                logger.warning(
                    f"Skipping inscription with missing required fields. "
                    f"inscription_id: {inscription_id}, "
                    f"inscription_number: {inscription_number}, "
                    f"txid: {txid}"
                )
                continue

            yield NftToken.from_api(
                ident=inscription_id,
                collection='ordinals',
                collection_name='Bitcoin Ordinals',
                contract=txid,
                standard='ordinals',
                name=f"Ordinal #{inscription_number}",
                description='',
                amount=1,
                image_url='',
                metadata_url=None,
                updated_time=inscription.get('timestamp'),
                is_disabled=False,
                is_nsfw=False,
                blockchain=Blockchain.BITCOIN,
                asset_type=AssetType.AVAILABLE,
                market_url=None,
            )

    def fetch_collection(self, collection: str) -> FetchResult:
        """
        Fetch collection information and items

        Args:
            collection: Collection ID to fetch

        Returns:
            FetchResult containing collection data and items
        """
        if not collection:
            raise ValueError("Collection ID is required")

        try:
            info_response = self.get_data(
                'get_collection',
                headers=self.headers,
                collectionId=collection,
            )
            info = FetchResult(
                data=info_response.get('data', {}) if info_response else {}
            )

            items_response = self.get_data(
                'get_collection_items',
                headers=self.headers,
                collectionId=collection,
            )
            items = FetchResult(
                data=items_response.get('data', {}) if items_response else {}
            )

            stats_response = self.post(
                'get_collection_stats',
                headers=self.headers,
                json={'collectionId': collection},
            )
            stats = FetchResult(
                data=stats_response.get('data', {}) if stats_response else {}
            )

            return FetchResult.from_fetch_results(info=info, items=items, stats=stats)
        except (HTTPError, ValueError, TypeError, AttributeError) as e:
            logger.error(f"Error fetching collection {collection}: {str(e)}")
            return FetchResult(errors=[str(e)])

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
            info = fetch_result.data.get('info', {})
            items = fetch_result.data.get('items', {})
            stats = fetch_result.data.get('stats', {})

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
                data=[collection] if collection else None,
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
