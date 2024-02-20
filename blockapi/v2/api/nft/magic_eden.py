import logging
from decimal import Decimal
from typing import Iterable, Optional, Tuple

from blockapi.v2.base import BlockchainApi, INftParser, INftProvider
from blockapi.v2.coins import COIN_SOL
from blockapi.v2.models import (
    ApiOptions,
    AssetType,
    Blockchain,
    Coin,
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


class MagicEdenApi(BlockchainApi, INftProvider, INftParser):
    """
    API docs: https://docs.magiceden.io/reference/solana-overview
    Explorer: https://magiceden.io/
    """

    blockchain: Blockchain = NotImplemented

    api_options = ApiOptions(
        blockchain=blockchain,
        base_url='https://api-mainnet.magiceden.dev/v2/',
        rate_limit=0.5,  # ~2 per second
    )

    supported_requests = {
        'get_nfts': 'wallets/{address}/tokens?offset={offset}&limit={limit}',
        'get_collection': 'collections/{slug}/stats',
        'get_listings': 'collections/{slug}/listings?offset={offset}&limit={limit}',
        'get_activities': 'collections/{slug}/activities?offset={offset}&limit={limit}',
        'get_pools': 'mmm/pools?collectionSymbol={slug}&showInvalid=false&offset={offset}&limit={limit}&filterOnSide=0&hideExpired=true&direction=1&field=5&attributesMode=0&attributes=[]&enableSNS=true',
    }

    coin_map = NotImplemented

    def __init__(self, sleep_provider):
        super().__init__()

        self._sleep_provider = sleep_provider

    def fetch_nfts(self, address: str) -> FetchResult:
        offset = 0
        limit = 500
        items = []

        while True:
            self._sleep_provider.sleep(self.base_url, self.api_options.rate_limit)
            data = self.get_data(
                'get_nfts',
                address=address,
                limit=limit,
                offset=offset,
            )

            if self._should_retry(data):
                continue

            if data.data:
                items.extend(data.data)
                offset += limit

            if data.errors or not data.data or len(data.data) < limit or offset > 15000:
                return FetchResult(
                    status_code=data.status_code,
                    headers=data.headers,
                    data=items,
                    errors=data.errors,
                    extra=data.extra,
                    time=data.time,
                )

    def parse_nfts(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result or not fetch_result.data:
            return ParseResult()

        parsed = list(self._yield_parsed_nfts(fetch_result.data))
        return ParseResult(
            data=parsed, errors=fetch_result.errors, cursor=fetch_result.cursor
        )

    def _yield_parsed_nfts(self, data) -> Iterable[NftToken]:
        for item in data:
            yield NftToken.from_api(
                ident=item.get('mintAddress'),
                collection=item.get('collection'),
                contract=item.get('collection'),
                standard='erc721',
                name=item.get('name'),
                description=None,
                amount=self._parse_supply(item.get('supply')),
                image_url=item.get('image'),
                metadata_url=None,
                updated_time=None,
                is_disabled=False,
                is_nsfw=False,
                blockchain=self.blockchain,
                asset_type=AssetType.AVAILABLE,
                collection_name=item.get('collectionName'),
            )

    @staticmethod
    def _parse_supply(s: str):
        try:
            return int(s)
        except ValueError as e:
            logger.warning(f'Supply cannot be parsed: {s}: {str(e)}')
            return 1

    def fetch_collection(self, collection: str) -> FetchResult:
        while True:
            self._sleep_provider.sleep(self.base_url, self.api_options.rate_limit)

            data = self.get_data(
                'get_collection',
                slug=collection,
            )

            if self._should_retry(data):
                continue

            return data

    def parse_collection(self, fetch_result: FetchResult) -> ParseResult:
        item = fetch_result.data
        if not item:
            return ParseResult(errors=fetch_result.errors)

        parsed = NftCollection.from_api(
            ident=item.get('symbol'),
            name=item.get('symbol'),
            contracts=[
                ContractInfo.from_api(
                    blockchain=self.blockchain, address=item.get('symbol')
                )
            ],
            image=None,
            is_disabled=False,
            is_nsfw=False,
            blockchain=self.blockchain,
            total_stats=NftCollectionTotalStats.from_api_convert_decimals(
                volume=item.get('volumeAll'),
                sales_count='0',
                owners_count='0',
                market_cap='0',
                floor_price=item.get('floorPrice'),
                average_price=item.get('avgPrice24hr'),
                coin=COIN_SOL,
            ),
            day_stats=None,
            week_stats=None,
            month_stats=None,
        )

        return ParseResult(
            data=[parsed] if parsed else None, errors=fetch_result.errors
        )

    def fetch_offers(
        self, collection: str, cursor: Optional[str] = None
    ) -> FetchResult:
        offset = 0
        limit = 500
        items = []

        while True:
            self._sleep_provider.sleep(self.base_url, self.api_options.rate_limit)
            logger.info(f'get_pools: {collection} offset={offset} limit={limit}')
            data = self.get_data(
                'get_pools', slug=collection, offset=offset, limit=limit
            )

            if self._should_retry(data):
                continue

            data_len = 0
            if data.data:
                results = data.data.get('results')
                items.extend(results)
                data_len = len(results)
                offset += limit

            if data.errors or not data.data or data_len < limit or offset > 15000:
                return FetchResult(
                    status_code=data.status_code,
                    headers=data.headers,
                    data=items,
                    errors=data.errors,
                    extra=data.extra,
                    time=data.time,
                )

    def parse_offers(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result or not fetch_result.data:
            return ParseResult(errors=fetch_result.errors if fetch_result else None)

        return ParseResult(
            data=list(self._yield_parsed_offers(fetch_result.data)),
            errors=fetch_result.errors,
        )

    def _yield_parsed_offers(self, items: list[dict]) -> Iterable[NftOffer]:
        seen = set()

        for item in items:
            key = item.get('uuid')
            if key in seen:
                continue

            amount = self._get_offer_price(item)
            coin = COIN_SOL
            start_time = item.get('updatedAt')
            pay_amount = item.get('buyOrdersAmount')

            if not pay_amount:
                continue

            seen.add(key)

            yield NftOffer.from_api(
                offer_key=key,
                direction=NftOfferDirection.OFFER,
                collection=item.get('collectionSymbol'),
                contract=item.get('collectionSymbol'),
                blockchain=self.blockchain,
                offerer=item.get('poolOwner'),
                start_time=start_time,
                end_time=None,
                offer_coin=coin,
                offer_contract=None,
                offer_ident=None,
                offer_amount=amount,
                pay_coin=None,
                pay_contract=item.get('collectionSymbol'),
                pay_ident=None,
                pay_amount=pay_amount,
            )

    def _get_offer_price(self, item: dict) -> str:
        # details: https://docs.magiceden.io/reference/mmm-pool-pricing
        spot_price = Decimal(item.get('spotPrice'))
        seller_fee = Decimal(item.get('collectionSellerFeeBasisPoints', 0)) / 10000
        lp_fee = Decimal(item.get('lpFeeBp', 0)) / 10000
        takers_fee = Decimal('0.0225')
        return str(spot_price * (1 - seller_fee - takers_fee - lp_fee))

    def fetch_listings(
        self, collection: str, cursor: Optional[str] = None
    ) -> FetchResult:
        offset = 0
        limit = 100
        items = []

        while True:
            self._sleep_provider.sleep(self.base_url, self.api_options.rate_limit)
            data = self.get_data(
                'get_listings', slug=collection, offset=offset, limit=limit
            )

            if self._should_retry(data):
                continue

            if data.data:
                items.extend(data.data)
                offset += limit

            # note: if offset is greater than 15000, causes response "offset should be non-negative integer"
            if data.errors or not data.data or len(data.data) < limit or offset > 15000:
                return FetchResult(
                    status_code=data.status_code,
                    headers=data.headers,
                    data=items,
                    errors=data.errors,
                    extra=data.extra,
                    time=data.time,
                )

    def parse_listings(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result:
            return ParseResult()

        return ParseResult(
            data=list(self._yield_parsed_listings(fetch_result.data)),
            errors=fetch_result.errors,
        )

    def _yield_parsed_listings(self, items: list[dict]) -> Iterable[NftOffer]:
        if not items:
            return

        seen = set()
        for item in items:
            key = self._get_listing_key(item)
            if key in seen:
                continue

            token = item.get('token')
            if not token:
                logger.info(
                    f'Token not found for listing signature {item.get("signature")}'
                )
                continue

            coin, amount = self._get_listing_price(item)
            if not coin:
                logger.info(
                    f'No coin mapped for listing signature {item.get("signature")}'
                )

            if not amount:
                continue

            seen.add(key)

            yield NftOffer.from_api(
                offer_key=key,
                direction=NftOfferDirection.LISTING,
                collection=token.get('collection'),
                contract=token.get('collection'),
                blockchain=self.blockchain,
                offerer=item.get('seller'),
                start_time='0',
                end_time=None,
                offer_coin=None,
                offer_contract=token.get('collection'),
                offer_ident=item.get('tokenMint'),
                offer_amount=item.get('tokenSize'),
                pay_coin=coin,
                pay_contract=None,
                pay_ident=None,
                pay_amount=amount,
            )

    def _get_listing_key(self, item) -> str:
        token = item.get('token')
        collection = token.get('collection') if token else item.get('collection')
        mint = item.get('tokenMint', '')
        user = item.get('seller', '') or item.get('buyer')

        return f'{collection}_{mint}_{user}'

    def _get_listing_price(self, item) -> Tuple[Optional[Coin], Optional[str]]:
        if priceInfo := item.get('priceInfo'):
            if price := priceInfo.get('solPrice'):
                return self.coin_map.get(price.get('address')), price.get('rawAmount')

        return None, None

    def _should_retry(self, data: FetchResult) -> bool:
        if not data.errors:
            return False

        retry = bool(
            [t for t in data.errors if str(t).upper() == 'SERVICE UNAVAILABLE']
        )
        if retry:
            logger.warning('Service unavailable - will retry after long sleep')
            self._sleep_provider.sleep(self.base_url, seconds=60)
            return True

        return False


class MagicEdenSolanaApi(MagicEdenApi):
    blockchain = Blockchain.SOLANA
    coin_map = {'So11111111111111111111111111111111111111112': COIN_SOL}
