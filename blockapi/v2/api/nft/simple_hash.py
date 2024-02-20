import logging
from typing import Iterable, Optional

from blockapi.v2.base import BlockchainApi, INftParser, INftProvider
from blockapi.v2.coins import COIN_BTC
from blockapi.v2.models import (
    ApiOptions,
    AssetType,
    Blockchain,
    ContractInfo,
    FetchResult,
    NftCollection,
    NftCollectionTotalStats,
    NftOffer,
    NftOfferDirection,
    NftToken,
    ParseResult,
)

logger = logging.getLogger(__name__)


class SimpleHashApi(BlockchainApi, INftProvider, INftParser):
    """
    API docs: https://docs.simplehash.com/reference/overview
    Explorer: https://magiceden.io/
    """

    coin = COIN_BTC
    blockchain = Blockchain.BITCOIN
    native_coin_id = 'bitcoin.native'
    inscriptions_collection = 'inscriptions'

    api_options = ApiOptions(
        blockchain=blockchain,
        base_url='https://api.simplehash.com/api/v0/nfts/',
        rate_limit=0.5,  # 2 per second
    )

    supported_requests = {
        'get_nfts': 'owners?chains={chain}&wallet_addresses={address}',
        'get_collection': 'collections/ids?collection_ids={slug}',
        'get_bids': 'bids/collection/{slug}',
        'get_listings': 'listings/collection/{slug}',
    }

    def __init__(self, api_key):
        super().__init__()

        self._api_key = api_key
        self.headers = {'accept': 'application/json', 'X-API-KEY': api_key}

    def fetch_nfts(self, address: str, cursor: Optional[str] = None) -> FetchResult:
        return self.get_data(
            'get_nfts',
            headers=self.headers,
            params=dict(cursor=cursor) if cursor else None,
            chain=self.blockchain,
            address=address,
        )

    def parse_nfts(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result or not fetch_result.data:
            return ParseResult(errors=fetch_result.errors if fetch_result else None)

        parsed = list(self._yield_parsed_nfts(fetch_result.data))
        return ParseResult(
            data=parsed,
            errors=fetch_result.errors,
            cursor=fetch_result.data.get('next_cursor'),
        )

    def _yield_parsed_nfts(self, data):
        items = data.get('nfts')
        if not items:
            return

        for item in items:
            collection = item.get('collection')
            contract = item.get('contract')
            ident = item.get('nft_id')

            if not ident:
                continue

            collection_id = (
                collection.get('collection_id') or self.inscriptions_collection
            )
            yield NftToken.from_api(
                ident=ident,
                collection=collection_id,
                contract=collection_id,
                standard=contract.get('type', 'ordinals').lower(),
                name=item.get('name') or contract.get('name'),
                description=None,
                amount=item.get('owner_count'),
                image_url=item.get('image_url'),
                metadata_url=None,
                updated_time=item.get('created_date'),
                is_disabled=False,
                is_nsfw=False,
                blockchain=self.blockchain,
                asset_type=AssetType.AVAILABLE,
            )

    def fetch_collection(self, collection: str) -> FetchResult:
        if collection == self.inscriptions_collection:
            return FetchResult(
                data=dict(
                    collections=[
                        dict(
                            collection_id=self.inscriptions_collection,
                            name='Inscriptions',
                        )
                    ]
                )
            )

        return self.get_data(
            'get_collection',
            headers=self.headers,
            slug=collection,
        )

    def parse_collection(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result or not fetch_result.data:
            return ParseResult(errors=fetch_result.errors if fetch_result else None)

        items = fetch_result.data.get('collections')
        item = items[0]
        parsed = NftCollection.from_api(
            ident=item.get('collection_id'),
            name=item.get('name'),
            contracts=[
                ContractInfo.from_api(
                    blockchain=self.blockchain, address=item.get('collection_id')
                )
            ],
            image=item.get('image_url'),
            is_disabled=False,
            is_nsfw=False,
            blockchain=self.blockchain,
            total_stats=NftCollectionTotalStats.from_api_convert_decimals(
                volume=item.get('volumeAll'),
                sales_count='0',
                owners_count='0',
                market_cap='0',
                floor_price=self.get_price(item.get('floor_prices')),
                average_price='0',
                coin=COIN_BTC,
            ),
            day_stats=None,
            week_stats=None,
            month_stats=None,
        )

        return ParseResult(
            data=[parsed] if parsed else None, errors=fetch_result.errors
        )

    def get_price(self, items):
        if not items:
            return '0'

        for item in items:
            if token := item.get('payment_token'):
                if token_id := token.get('payment_token_id'):
                    if token_id == self.native_coin_id:
                        return item.get('value')

        return '0'

    def fetch_offers(
        self, collection: str, cursor: Optional[str] = None
    ) -> FetchResult:
        return self.get_data(
            'get_bids',
            headers=self.headers,
            params=dict(cursor=cursor) if cursor else None,
            slug=collection,
        )

    def parse_offers(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result or not fetch_result.data:
            return ParseResult(errors=fetch_result.errors if fetch_result else None)

        return ParseResult(
            data=list(self._yield_parsed_offers(fetch_result.data.get('bids'))),
            cursor=fetch_result.data.get('next_cursor'),
            errors=fetch_result.errors,
        )

    def _yield_parsed_offers(self, items: list[dict]) -> Iterable[NftOffer]:
        if not items:
            return

        for item in items:
            if (
                item.get('payment_token', dict()).get('payment_token_id')
                != self.native_coin_id
            ):
                continue

            if item.get('is_private') == 'true':
                continue

            yield NftOffer.from_api(
                offer_key=item.get('id'),
                direction=NftOfferDirection.OFFER,
                collection=item.get('collection_id'),
                contract=item.get('collection_id'),
                blockchain=self.blockchain,
                offerer=item.get('bidder_address'),
                start_time=item.get('timestamp'),
                end_time=item.get('expiration_timestamp'),
                offer_coin=COIN_BTC,
                offer_amount=item.get('price'),
                offer_contract=None,
                offer_ident=None,
                pay_contract=item.get('collection_id'),
                pay_ident=item.get('nft_id'),
                pay_amount=item.get('quantity'),
                pay_coin=None,
            )

    def fetch_listings(
        self, collection: str, cursor: Optional[str] = None
    ) -> FetchResult:
        return self.get_data(
            'get_listings',
            headers=self.headers,
            params=dict(cursor=cursor) if cursor else None,
            slug=collection,
        )

    def parse_listings(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result or not fetch_result.data:
            return ParseResult(errors=fetch_result.errors if fetch_result else None)

        return ParseResult(
            data=list(self._yield_parsed_listings(fetch_result.data.get('listings'))),
            cursor=fetch_result.data.get('next_cursor'),
            errors=fetch_result.errors,
        )

    def _yield_parsed_listings(self, items: list[dict]) -> Iterable[NftOffer]:
        if not items:
            return

        for item in items:
            if (
                item.get('payment_token', dict()).get('payment_token_id')
                != self.native_coin_id
            ):
                continue

            if item.get('is_private') == 'true':
                continue

            yield NftOffer.from_api(
                offer_key=item.get('id'),
                direction=NftOfferDirection.LISTING,
                collection=item.get('collection_id'),
                contract=item.get('collection_id'),
                blockchain=self.blockchain,
                offerer=item.get('seller_address'),
                start_time=item.get('listing_timestamp'),
                end_time=item.get('expiration_timestamp'),
                offer_coin=None,
                offer_amount=item.get('quantity'),
                offer_contract=item.get('collection_id'),
                offer_ident=item.get('nft_id'),
                pay_contract=None,
                pay_ident=None,
                pay_amount=item.get('price'),
                pay_coin=COIN_BTC,
            )
