import logging
from typing import Optional, Dict, Generator, Tuple
from enum import Enum
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
    NftOffer,
    NftOfferDirection,
    BtcNftType,
)
from blockapi.utils.num import raw_to_decimals
from requests import HTTPError
import requests

logger = logging.getLogger(__name__)


class NftSortBy(str, Enum):
    UNIT_PRICE = 'unitPrice'
    ON_SALE_TIME = 'onSaleTime'
    INIT_PRICE = 'initPrice'
    INSCRIPTION_NUMBER = 'inscriptionNumber'


class UnisatApi(BlockchainApi, INftParser, INftProvider):
    """
    API docs: https://docs.unisat.io/
    """

    coin = COIN_BTC

    DEFAULT_CID = "uncategorized-ordinals"
    DEFAULT_CNAME = "Uncategorized Ordinals"

    api_options = ApiOptions(
        blockchain=Blockchain.BITCOIN,
        base_url='https://open-api.unisat.io/',
        rate_limit=0.2,  # 5 calls per second for free tier
    )

    supported_requests = {
        'get_nfts': 'v1/indexer/address/{address}/inscription-data',
        'get_listings': 'v3/market/collection/auction/list',
        'get_offers': 'v3/market/collection/auction/actions',
        'get_collection_stats': 'v3/market/collection/auction/collection_statistic',
        'get_collection_summary': '/v3/market/collection/auction/collection_summary',
    }

    def __init__(
        self,
        api_key: str,
        sleep_provider: Optional[ISleepProvider] = None,
        limit: Optional[int] = 10000,
    ):
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
        self.limit = limit

        self._collection_map = None

    def fetch_nfts(self, address: str) -> FetchResult:
        """
        Fetch NFTs (inscriptions) owned by the address

        Args:
            address: BTC address to fetch NFTs for

        Returns:
            FetchResult containing the NFT data

        Raises:
            ValueError: If address is empty or invalid
        """
        if not address:
            raise ValueError("Address is required")

        params = {'size': self.limit, 'cursor': 0}

        try:
            result = self.get_data(
                'get_nfts',
                headers=self.headers,
                params=params,
                address=address,
                extra=dict(address=address),
            )

            if self._collection_map is None:
                self._collection_map = self._build_collection_map(address)

            return result
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

        if not fetch_result.data:
            errors.append("No data in fetch result")
            return ParseResult(data=[], errors=errors)

        if isinstance(fetch_result.data, dict) and "code" in fetch_result.data:
            api_code = fetch_result.data["code"]
            if api_code != 0:
                api_msg = fetch_result.data.get("msg", "Unknown error")
                errors.append(f"Unisat error {api_code}: {api_msg}")
                return ParseResult(data=[], errors=errors)

        inner_data = fetch_result.data.get("data", {})
        if not inner_data:
            errors.append("No data in API response")
            return ParseResult(data=[], errors=errors)

        if self._collection_map is None:
            errors.append("Collection map is not initialized.")
            return ParseResult(errors=[errors])

        for nft in self._yield_parsed_nfts(inner_data):
            data.append(nft)

        return ParseResult(data=data, errors=errors)

    def _yield_parsed_nfts(self, data: Dict) -> Generator[NftToken, None, None]:
        """Yield parsed NFT tokens from Unisat API response"""
        if not data or "inscription" not in data:
            logger.warning("No NFT data found in response")
            return

        for item in data["inscription"]:
            try:
                if not all(
                    k in item
                    for k in (
                        "inscriptionId",
                        "inscriptionNumber",
                        "timestamp",
                        "utxo",
                    )
                ):
                    logger.warning(f"Missing required fields in NFT data: {item}")
                    continue

                utxo = item["utxo"]
                if not all(k in utxo for k in ("txid", "address")):
                    logger.warning(f"Missing required fields in UTXO data: {utxo}")
                    continue

                iid = item["inscriptionId"]
                cid, cname = self._collection_map.get(
                    iid, (self.DEFAULT_CID, self.DEFAULT_CNAME)
                )

                yield NftToken.from_api(
                    ident=iid,
                    collection=cid,
                    collection_name=cname,
                    contract=cid,
                    standard="ordinals",
                    name=f"Ordinal #{item['inscriptionNumber']}",
                    description="",
                    amount=1,
                    image_url=f"https://open-api.unisat.io/v1/indexer/inscription/content/{iid}",
                    metadata_url=None,
                    updated_time=str(item["timestamp"]),
                    is_disabled=False,
                    is_nsfw=False,
                    blockchain=Blockchain.BITCOIN,
                    asset_type=AssetType.AVAILABLE,
                    market_url=None,
                )

            except Exception as e:
                logger.warning(f"Error parsing NFT item {item}: {str(e)}")
                continue

    def _build_collection_map(self, address: str) -> Dict[str, Tuple[str, str]]:
        """Return a mapping using a single collection_summary call.

        Raises
        ------
        ValueError
            If UniSat returns a non‑zero `code` (e.g. -119 = address invalid).
        """
        try:
            resp = self.post(
                "get_collection_summary",
                json={"address": address},
                headers=self.headers,
            )
        except Exception as exc:
            raise ValueError(f"UniSat request failed: {exc}") from exc

        if not isinstance(resp, dict):
            raise ValueError("Unexpected response object from UniSat")

        if resp.get("code", -1) != 0:
            raise ValueError(f"Unisat error {resp.get('code')}: {resp.get('msg')}")

        mapping: Dict[str, Tuple[str, str]] = {}
        for col in resp.get("data", {}).get("list", []):
            cid = col.get("collectionId", self.DEFAULT_CID)
            name = col.get("name", self.DEFAULT_CNAME)
            for iid in col.get("ids", []):
                mapping[iid] = (cid, name)
        return mapping

    def fetch_collection(self, collection: str) -> FetchResult:
        """Fetch collection data from Unisat API."""
        try:
            stats_data = self.post(
                'get_collection_stats',
                json={'collectionId': collection},
                headers=self.headers,
            )
            return FetchResult(data=stats_data)
        except (HTTPError, ValueError, TypeError) as e:
            logger.error(f"Error fetching collection {collection}: {str(e)}")
            return FetchResult(errors=[str(e)])
        except Exception as e:
            logger.error(f"Unexpected error fetching collection {collection}: {str(e)}")
            return FetchResult(errors=[str(e)])

    def parse_collection(self, fetch_result: FetchResult) -> ParseResult:
        """
        Parse collection data from the API response

        Args:
            fetch_result: Raw API response data

        Returns:
            ParseResult containing parsed collection data
        """
        if not fetch_result:
            return ParseResult(errors=["Empty response from UniSat"])

        unisat_response = fetch_result.data
        code = unisat_response.get("code", 0)

        # ----- dummy-result case ---------------------------------------
        if (
            code == -1
            and unisat_response.get("msg") == "Internal Server Error"
            and unisat_response.get("data") is None
        ):
            return self._dummy_result()

        # ----- any other UniSat error ------------------------------------------
        if code != 0:
            return ParseResult(errors=fetch_result.errors)

        stats = fetch_result.data.get("data", {})
        if not stats:
            return ParseResult(errors=["No collection data found in response"])

        collection_id = stats.get("collectionId")
        if not collection_id:
            return ParseResult(errors=["No collection ID found in response"])

        # Format the icon URL
        icon = stats.get("icon")
        icon_url = None

        if icon:
            if icon.startswith(("http://", "https://")):
                icon_url = icon
            else:
                icon_url = f"https://static.unisat.io/content/{icon.lstrip('/')}"

        floor_price = raw_to_decimals(stats.get("floorPrice", 0), self.coin.decimals)

        volume = raw_to_decimals(stats.get("btcValue", 0), self.coin.decimals)

        total_stats = NftCollectionTotalStats.from_api(
            volume=str(volume),
            sales_count=None,
            owners_count=None,
            market_cap=None,
            floor_price=str(floor_price),
            average_price=None,
            coin=self.coin,
        )

        collection = NftCollection.from_api(
            ident=collection_id,
            name=stats.get("name", f"Collection {collection_id}"),
            contracts=[
                ContractInfo.from_api(
                    blockchain=Blockchain.BITCOIN, address=collection_id
                )
            ],
            image=icon_url,
            is_disabled=False,
            is_nsfw=False,
            blockchain=Blockchain.BITCOIN,
            total_stats=total_stats,
            volumes=NftVolumes.from_api(coin=self.coin),
        )

        return ParseResult(data=[collection], errors=fetch_result.errors)

    def _dummy_result(self) -> ParseResult:
        dummy_stats = NftCollectionTotalStats.from_api(
            volume="0",
            sales_count="0",
            owners_count="0",
            market_cap="0",
            floor_price="0",
            average_price="0",
            coin=self.coin,
        )
        dummy_col = NftCollection.from_api(
            ident=self.DEFAULT_CID,
            name=self.DEFAULT_CNAME,
            contracts=[
                ContractInfo.from_api(
                    blockchain=Blockchain.BITCOIN, address=self.DEFAULT_CID
                )
            ],
            image=None,
            is_disabled=False,
            is_nsfw=False,
            blockchain=Blockchain.BITCOIN,
            total_stats=dummy_stats,
            volumes=NftVolumes.from_api(coin=self.coin),
        )
        return ParseResult(data=[dummy_col])

    def fetch_listings(
        self,
        nft_type: BtcNftType = BtcNftType.COLLECTION,
        collection: Optional[str] = None,
        limit: int = 499,
        address: Optional[str] = None,
        tick: Optional[str] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        nft_confirm: Optional[bool] = None,
        is_end: Optional[bool] = None,
        domain_type: Optional[str] = None,
        domain_min_length: Optional[int] = None,
        domain_max_length: Optional[int] = None,
        domain_category: Optional[str] = None,
        domain_fuzzy: Optional[str] = None,
        collection_fuzzy: Optional[str] = None,
        all_items: Optional[bool] = None,
        sort_by: NftSortBy = NftSortBy.UNIT_PRICE,
        sort_order: int = -1,
        cursor: Optional[str] = None,
    ) -> FetchResult:
        """
        Fetch all current listings (sell offers) for a specific collection.

        Args:
            nft_type: Type of NFT (brc20, domain, collection, arc20, runes)
            collection: Collection ID (slug), optional
            limit: Number of items per page
            address: Filter by address
            tick: Filter by tick (for BRC20)
            min_price: Minimum price filter
            max_price: Maximum price filter
            nft_confirm: Filter by confirmation status
            is_end: Filter by end status
            domain_type: Filter by domain type (e.g., 'sats')
            domain_min_length: Minimum domain length
            domain_max_length: Maximum domain length
            domain_category: Domain category filter
            domain_fuzzy: Domain fuzzy search
            collection_fuzzy: Collection fuzzy search
            all_items: Whether to fetch all items
            sort_by: Field to sort by (unitPrice, onSaleTime, initPrice, inscriptionNumber)
            sort_order: Sort order (1 for ascending, -1 for descending)

        Returns:
            FetchResult containing listing data
        """
        # Ensure we get the string value if an enum is passed
        nft_type_str = (
            nft_type.value if isinstance(nft_type, BtcNftType) else str(nft_type)
        )

        filter_dict = {"nftType": nft_type_str}

        if collection:
            filter_dict["collectionId"] = collection
        if address:
            filter_dict["address"] = address
        if tick:
            filter_dict["tick"] = tick
        if min_price is not None:
            filter_dict["minPrice"] = min_price
        if max_price is not None:
            filter_dict["maxPrice"] = max_price
        if nft_confirm is not None:
            filter_dict["nftConfirm"] = nft_confirm
        if is_end is not None:
            filter_dict["isEnd"] = is_end
        if domain_type:
            filter_dict["domainType"] = domain_type
        if domain_min_length is not None:
            filter_dict["domainMinLength"] = domain_min_length
        if domain_max_length is not None:
            filter_dict["domainMaxLength"] = domain_max_length
        if domain_category:
            filter_dict["domainCategory"] = domain_category
        if domain_fuzzy:
            filter_dict["domainFuzzy"] = domain_fuzzy
        if collection_fuzzy:
            filter_dict["collectionFuzzy"] = collection_fuzzy
        if all_items is not None:
            filter_dict["all"] = all_items

        sort_dict = {}
        sort_dict[sort_by] = sort_order

        if limit >= 500:
            logger.warning(
                f"Unisat API limit is 500. You tried to fetch {limit} items. Truncating to 499."
            )
            limit = 499

        request_body = {
            "filter": filter_dict,
            "sort": sort_dict,
            "start": 0,
            "limit": limit,
        }

        try:
            response_data = self.post(
                'get_listings', json=request_body, headers=self.headers
            )
            return FetchResult(data=response_data)
        except (HTTPError, ValueError, TypeError) as e:
            logger.error(f"Error fetching listings for nft_type {nft_type}: {str(e)}")
            return FetchResult(errors=[str(e)])
        except Exception as e:
            logger.error(
                f"Unexpected error fetching listings for nft_type {nft_type}: {str(e)}"
            )
            return FetchResult(errors=[str(e)])

    def parse_listings(self, fetch_result: FetchResult) -> ParseResult:
        """
        Parse listing data from API response.

        Args:
            fetch_result: Raw API response data from fetch_listings

        Returns:
            ParseResult containing parsed NftOffer objects
        """
        if not fetch_result or not fetch_result.data:
            return ParseResult(errors=fetch_result.errors if fetch_result else None)

        inner_data = fetch_result.data.get("data", {})
        if not inner_data:
            return ParseResult(errors=fetch_result.errors)

        items = inner_data.get("list", [])

        return ParseResult(
            data=list(self._yield_parsed_listings(items)),
            errors=fetch_result.errors,
        )

    def _yield_parsed_listings(
        self, items: list[Dict]
    ) -> Generator[NftOffer, None, None]:
        """Yield parsed NftOffer objects from listing items."""
        if not items:
            return

        for item in items:
            if not all(
                k in item for k in ['auctionId', 'inscriptionId', 'address', 'price']
            ):
                logger.warning(
                    f"Skipping listing item due to missing required fields: {item}"
                )
                continue

            collection_id = item.get('collectionId', '')

            amount = item.get('amount')
            if amount is None:
                amount = 1

            price_sat = item.get('price') or 0

            yield NftOffer.from_api(
                offer_key=item["auctionId"],
                direction=NftOfferDirection.LISTING,
                collection=collection_id,
                contract=collection_id,
                blockchain=Blockchain.BITCOIN,
                offerer=item["address"],
                start_time=None,
                end_time=None,
                offer_coin=None,
                offer_amount=amount,
                offer_contract=collection_id,
                offer_ident=item["inscriptionId"],
                pay_contract=None,
                pay_ident=None,
                pay_amount=price_sat,
                pay_coin=self.coin,
            )

    def fetch_offers(
        self,
        nft_type: BtcNftType = BtcNftType.COLLECTION,
        address: Optional[str] = None,
        inscription_id: Optional[str] = None,
        event: Optional[str] = None,
        tick: Optional[str] = None,
        domain_type: Optional[str] = None,
        collection: Optional[str] = None,
        limit: int = 499,
        cursor: Optional[str] = None,
    ) -> FetchResult:
        """
        Fetch listing events (historical or recent) in a collection.

        Args:
            nft_type: Type of NFT (brc20, domain, collection, arc20, runes)
            address: Filter by address
            inscription_id: Filter by inscription ID
            event: Filter by event type (Listed, Cancel, Buy)
            tick: Filter by tick (for BRC20)
            domain_type: Filter by domain type
            collection: Collection ID to filter by
            limit: Number of items

        Returns:
            FetchResult containing the listing action data
        """
        # Ensure we get the string value if an enum is passed
        nft_type_str = (
            nft_type.value if isinstance(nft_type, BtcNftType) else str(nft_type)
        )

        filter_dict = {}
        if nft_type_str:
            filter_dict["nftType"] = nft_type_str
        if address:
            filter_dict["address"] = address
        if inscription_id:
            filter_dict["inscriptionId"] = inscription_id
        if event:
            filter_dict["event"] = event
        if tick:
            filter_dict["tick"] = tick
        if domain_type:
            filter_dict["domainType"] = domain_type
        if collection:
            filter_dict["collectionId"] = collection

        if limit >= 500:
            logger.warning(
                f"Unisat API limit is 500. You tried to fetch {limit} items. Truncating to 499."
            )
            limit = 499

        request_body = {
            "filter": filter_dict,
            "start": 0,
            "limit": limit,
        }

        try:
            response_data = self.post(
                'get_offers', json=request_body, headers=self.headers
            )
            return FetchResult(data=response_data)
        except (HTTPError, ValueError, TypeError) as e:
            logger.error(f"Error fetching listing actions: {str(e)}")
            return FetchResult(errors=[str(e)])
        except Exception as e:
            logger.error(f"Unexpected error fetching listing actions: {str(e)}")
            return FetchResult(errors=[str(e)])

    def parse_offers(self, fetch_result: FetchResult) -> ParseResult:
        """
        Parse listing action data from API response.

        Args:
            fetch_result: Raw API response data from fetch_listing_actions

        Returns:
            ParseResult containing parsed NftOffer objects
        """
        if not fetch_result or not fetch_result.data:
            return ParseResult(errors=fetch_result.errors if fetch_result else None)

        inner_data = fetch_result.data.get("data", {})
        if not inner_data:
            return ParseResult(errors=fetch_result.errors)

        items = inner_data.get("list", [])

        return ParseResult(
            data=list(self._yield_parsed_offers(items)),
            errors=fetch_result.errors,
        )

    def _yield_parsed_offers(
        self, items: list[Dict]
    ) -> Generator[NftOffer, None, None]:
        """Yield parsed NftOffer objects from listing action items."""
        if not items:
            return

        for item in items:
            if not all(k in item for k in ['auctionId', 'inscriptionId', 'event']):
                logger.warning(
                    f"Skipping listing action due to missing required fields: {item}"
                )
                continue

            # Skip if not a listing event
            event = item.get('event')
            if event != 'Listed':
                continue

            collection_id = item.get('collectionId', '')

            # Handle amount - use 1 as default for null values
            amount = item.get('amount')
            if amount is None:
                amount = 1

            # Convert from milliseconds to ISO format
            timestamp = item.get('timestamp')
            formatted_time = None
            if timestamp:
                try:
                    timestamp_seconds = timestamp / 1000
                    formatted_time = datetime.fromtimestamp(
                        timestamp_seconds
                    ).isoformat()
                except (ValueError, TypeError, OverflowError):
                    logger.warning(
                        f"Could not parse timestamp {timestamp} for item {item.get('auctionId')}"
                    )

            price_sat = item.get('price') or 0

            yield NftOffer.from_api(
                offer_key=item["auctionId"],
                direction=NftOfferDirection.OFFER,
                collection=collection_id,
                contract=collection_id,
                blockchain=Blockchain.BITCOIN,
                offerer=item.get("from", ""),
                start_time=formatted_time,
                end_time=None,
                offer_coin=None,
                offer_amount=amount,
                offer_contract=collection_id,
                offer_ident=item["inscriptionId"],
                pay_contract=None,
                pay_ident=None,
                pay_amount=price_sat,
                pay_coin=self.coin,
            )
