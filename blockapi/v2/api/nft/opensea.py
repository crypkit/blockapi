import functools
import logging
from decimal import Decimal
from typing import Callable, Iterable, Optional, Tuple

from blockapi.utils.num import raw_to_decimals
from blockapi.v2.base import (
    ApiException,
    BlockchainApi,
    INftParser,
    INftProvider,
    ISleepProvider,
    SleepProvider,
)
from blockapi.v2.coin_mapping import OPENSEA_COINS, OPENSEA_CONTRACTS
from blockapi.v2.coins import COIN_ETH
from blockapi.v2.models import (
    ApiOptions,
    AssetType,
    Blockchain,
    Coin,
    ContractInfo,
    FetchResult,
    NftCollection,
    NftCollectionIntervalStats,
    NftCollectionTotalStats,
    NftOffer,
    NftOfferDirection,
    NftToken,
    OfferItemType,
    ParseResult,
)

logger = logging.getLogger(__name__)

OFFER_ITEM_TYPES = {
    '0': OfferItemType.NATIVE,
    '1': OfferItemType.ERC20,
    '2': OfferItemType.ERC721,
    '3': OfferItemType.ERC1155,
    '4': OfferItemType.ERC721_WITH_CRITERIA,
    '5': OfferItemType.ERC1155_WITH_CRITERIA,
}

OFFER_DIRECTION_KEYS = {
    NftOfferDirection.OFFER: 'offers',
    NftOfferDirection.LISTING: 'listings',
}


class OpenSeaApi(BlockchainApi, INftProvider, INftParser):
    """
    Ethereum
    API docs: https://docs.opensea.io/reference/api-overview
    Explorer: https://opensea.io/
    """

    supported_blockchains_map = {
        Blockchain.ARBITRUM: 'arbitrum',
        Blockchain.ARBITRUM_NOVA: 'arbitrum_nova',
        Blockchain.AVALANCHE: 'avalanche',
        Blockchain.BASE: 'base',
        Blockchain.BINANCE_SMART_CHAIN: 'bsc',
        Blockchain.ETHEREUM: 'ethereum',
        Blockchain.KLAYTN_CYPRESS: 'klaytn',
        Blockchain.OPTIMISM: 'optimism',
        Blockchain.POLYGON: 'matic',
        Blockchain.ZORA: 'zora',
    }

    opensea_blockchains_map = {n: b for b, n in supported_blockchains_map.items()}

    supported_blockchains = list(supported_blockchains_map.keys())

    coin = COIN_ETH
    api_options = ApiOptions(
        blockchain=Blockchain.ETHEREUM,
        base_url='https://api.opensea.io/',
        rate_limit=0.25,  # 4 per second
    )

    supported_requests = {
        'get_nfts': 'api/v2/chain/{chain}/account/{address}/nfts',
        'get_offers': 'api/v2/offers/collection/{collection}/all',
        'get_listings': 'api/v2/listings/collection/{collection}/all',
        'get_collection': 'api/v2/collections/{collection}',
        'get_collection_stats': 'api/v2/collections/{collection}/stats',
    }

    json_parse_args = dict(
        parse_int=lambda x: x,
        parse_float=lambda x: x,
    )

    def __init__(
        self,
        api_key: str,
        blockchain: Blockchain,
        sleep_provider: ISleepProvider = None,
        limit: Optional[int] = None,
    ):
        super().__init__(api_key)

        self._blockchain = blockchain
        self._opensea_chain = self.supported_blockchains_map.get(blockchain)
        if not self._opensea_chain:
            raise ApiException(f"Blockchain '{blockchain.value}' is not supported")

        self._headers = {'accept': 'application/json', 'x-api-key': api_key}
        self._sleep_provider = sleep_provider or SleepProvider()
        self._limit = limit

    def fetch_nfts(self, address: str, cursor: Optional[str] = None) -> FetchResult:
        logger.info(f'Fetch nfts from {address}, cursor={cursor}')
        return self._coalesce(self._yield_nfts(address, cursor))

    def parse_nfts(self, fetch_result: FetchResult) -> ParseResult:
        logger.info(f'Parse nfts')

        if not fetch_result:
            return ParseResult()

        parsed = list(self._yield_parsed_nfts(fetch_result.data))
        return ParseResult(
            data=parsed, errors=fetch_result.errors, cursor=fetch_result.cursor
        )

    def fetch_offers(
        self, collection: str, cursor: Optional[str] = None
    ) -> FetchResult:
        logger.info(f'Fetch offers from {collection}, cursor={cursor}')
        return self._coalesce(self._yield_offers(collection, cursor))

    def parse_offers(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result:
            return ParseResult()

        parsed = list(
            self._yield_parsed_offers(
                NftOfferDirection.OFFER, fetch_result.data, fetch_result.extra
            )
        )
        return ParseResult(
            data=parsed, errors=fetch_result.errors, cursor=fetch_result.cursor
        )

    def fetch_listings(
        self, collection: str, cursor: Optional[str] = None
    ) -> FetchResult:
        logger.info(f'Fetch listings from {collection}, cursor={cursor}')
        return self._coalesce(self._yield_listings(collection, cursor))

    def parse_listings(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result:
            return ParseResult()

        parsed = list(
            self._yield_parsed_offers(
                NftOfferDirection.LISTING,
                fetch_result.data,
                fetch_result.extra,
            )
        )
        return ParseResult(
            data=parsed, errors=fetch_result.errors, cursor=fetch_result.cursor
        )

    def fetch_collection(self, collection: str) -> FetchResult:
        while True:
            stats = self.get_data(
                'get_collection_stats',
                headers=self._headers,
                collection=collection,
                chain=self._opensea_chain,
            )

            if not self._should_retry(stats):
                break

        while True:
            result = self.get_data(
                'get_collection',
                headers=self._headers,
                collection=collection,
                chain=self._opensea_chain,
                extra=dict(
                    collection=collection, stats=stats.data, stats_errors=stats.errors
                ),
            )

            if not self._should_retry(result):
                return result

    def parse_collection(self, fetch_result: FetchResult) -> ParseResult:
        parsed, error = self._parse_collection(
            fetch_result.extra.get('collection'),
            fetch_result.data,
            fetch_result.extra.get('stats'),
        )
        errors = []
        if error:
            errors.append(error)

        if stats_errors := fetch_result.extra['stats_errors']:
            errors.append(stats_errors)

        return ParseResult(
            data=[parsed] if parsed else None, errors=errors if errors else None
        )

    def _yield_nfts(
        self, address: str, cursor: Optional[str] = None
    ) -> Iterable[Tuple[FetchResult, Optional[str]]]:
        try:
            yield from self._yield_fetch_data(
                self._fetch_nfts_page, key=address, cursor=cursor
            )
        except Exception as e:
            logger.error(f'Error fetching OpenSea NFTs from {address}')
            logger.exception(e)
            yield FetchResult(
                errors=[f'Error fetching OpenSea NFTs from {address}: {e}']
            ), None

    def _yield_offers(
        self, collection: str, cursor: Optional[str]
    ) -> Iterable[Tuple[FetchResult, Optional[str]]]:
        try:
            fetch_page = functools.partial(self._fetch_offers_page, 'get_offers')
            yield from self._yield_fetch_data(fetch_page, key=collection, cursor=cursor)
        except Exception as e:
            logger.error(f'Error fetching OpenSea collection {collection} offers')
            logger.exception(e)
            yield FetchResult(
                errors=[f'Error fetching OpenSea collection {collection} offers: {e}'],
                extra=dict(collection=collection),
            ), None

    def _yield_listings(
        self, collection: str, cursor: Optional[str]
    ) -> Iterable[Tuple[FetchResult, Optional[str]]]:
        try:
            fetch_page = functools.partial(self._fetch_offers_page, 'get_listings')
            yield from self._yield_fetch_data(fetch_page, key=collection, cursor=cursor)
        except Exception as e:
            logger.error(f'Error fetching OpenSea collection {collection} listings')
            logger.exception(e)
            yield FetchResult(
                errors=[
                    f'Error fetching OpenSea collection {collection} listings: {e}'
                ],
                extra=dict(collection=collection),
            ), None

    def _yield_fetch_data(
        self, fetch_method: Callable, key: str, cursor: Optional[str] = None
    ) -> Iterable[Tuple[FetchResult, Optional[str]]]:
        cursors = set()

        count = 0
        while True:
            self._sleep_provider.sleep(self.base_url, self.api_options.rate_limit)
            count += 1
            logger.debug(f'Fetching page {count} of {key} from {cursor}')
            fetched, next_cursor = fetch_method(key, cursor)
            if self._should_retry(fetched):
                count -= 1
                continue

            yield fetched, next_cursor

            if not next_cursor:
                break

            cursor = next_cursor
            if cursor in cursors:
                raise ApiException(f'Detected duplicate cursor {cursor}')

            cursors.add(cursor)

            if self._limit and count >= self._limit:
                break

    def _fetch_offers_page(
        self, method: str, collection: str, cursor: Optional[str] = None
    ) -> tuple[FetchResult, Optional[str]]:
        params = dict(next=cursor) if cursor else dict()

        fetched = self.get_data(
            method,
            headers=self._headers,
            params=params,
            collection=collection,
            chain=self._opensea_chain,
            extra=dict(collection=collection),
        )

        cursor = fetched.data.get('next') if fetched.data else None
        return fetched, cursor

    def _fetch_nfts_page(
        self, address: str, cursor: Optional[str] = None
    ) -> tuple[FetchResult, Optional[str]]:
        params = dict(next=cursor) if cursor else dict()
        fetched = self.get_data(
            'get_nfts',
            headers=self._headers,
            params=params,
            address=address,
            chain=self._opensea_chain,
        )

        cursor = fetched.data.get('next') if fetched.data else None
        return fetched, cursor

    def _yield_parsed_nfts(self, results):
        if not results:
            return

        for data in results:
            items = data.get('nfts')

            if not items:
                continue

            for item in items:
                yield NftToken.from_api(
                    ident=item.get('identifier'),
                    collection=item.get('collection'),
                    contract=item.get('contract'),
                    standard=item.get('token_standard'),
                    name=item.get('name'),
                    description=item.get('description'),
                    amount=item.get('amount'),
                    image_url=item.get('image_url'),
                    metadata_url=item.get('metadata_url'),
                    updated_time=item.get('updated_at'),
                    is_disabled=item.get('is_disabled'),
                    is_nsfw=item.get('is_nsfw'),
                    blockchain=self._blockchain,
                    asset_type=AssetType.AVAILABLE,
                )

    def _parse_collection(
        self, collection_ident: str, data: dict, stat_data: dict
    ) -> tuple[Optional[NftCollection], Optional[str]]:
        if not stat_data or not data:
            logger.warning(f'No data for collection: {collection_ident}')
            return None, None

        total = stat_data.get('total')
        symbol = total.get('floor_price_symbol')
        coin = OPENSEA_COINS.get(symbol)
        if not coin:
            coin = COIN_ETH
            if symbol:
                return (
                    None,
                    f'There is no mapping for opensea symbol {symbol} (collection={collection_ident})',
                )

        total_stats = NftCollectionTotalStats.from_api(
            volume=total.get('volume'),
            sales_count=total.get('sales'),
            owners_count=total.get('num_owners'),
            market_cap=total.get('market_cap'),
            floor_price=total.get('floor_price'),
            average_price=total.get('average_price'),
            coin=coin,
        )

        intervals = stat_data.get('intervals')
        day_stats = self._parse_collection_stats(intervals, 'one_day')
        week_stats = self._parse_collection_stats(intervals, 'one_week')
        month_stats = self._parse_collection_stats(intervals, 'one_month')

        contracts = list(self._yield_contracts(collection_ident, data.get('contracts')))

        collection = NftCollection.from_api(
            ident=data.get('collection'),
            name=data.get('name'),
            contracts=contracts,
            image=data.get('image_url'),
            is_disabled=data.get('is_disabled'),
            is_nsfw=data.get('is_nsfw'),
            total_stats=total_stats,
            day_stats=day_stats,
            week_stats=week_stats,
            month_stats=month_stats,
            blockchain=self._blockchain,
        )

        return collection, None

    @staticmethod
    def _parse_collection_stats(
        intervals, interval
    ) -> Optional[NftCollectionIntervalStats]:
        if not intervals:
            return None

        for it in intervals:
            if it.get('interval') != interval:
                continue

            st = NftCollectionIntervalStats.from_api(
                volume=it.get('volume'),
                volume_diff=it.get('volume_diff'),
                volume_percent_change=it.get('volume_change'),
                sales_count=it.get('sales'),
                sales_diff=it.get('sales_diff'),
                average_price=it.get('average_price'),
            )

            if st.volume == 0 and st.sales_count == 0:
                return

            return st

    def _yield_parsed_offers(
        self, direction: NftOfferDirection, results: list, extra: dict
    ) -> Iterable[NftOffer]:
        collection = extra.get('collection')
        contract = extra.get('contract')

        key = OFFER_DIRECTION_KEYS[direction]
        for result_item in results:
            if items := result_item.get(key):
                for item in items:
                    parsed = self._parse_offer(direction, collection, contract, item)
                    if parsed:
                        yield parsed

    def _parse_offer(
        self,
        direction: NftOfferDirection,
        collection: Optional[str],
        contract: Optional[str],
        item: dict,
    ) -> Optional[NftOffer]:
        params = self._get_offer_params(item)
        if not params:
            return None

        if not contract:
            contract = self._parse_contract(item)

        offerer = params.get('offerer')
        if not offerer:
            return None

        offerer = offerer.lower()

        offer = params.get('offer')
        if not offer:
            return None

        if len(offer) > 1:
            logger.warning(f'Multiple {direction} items: {collection} - {contract}')

        (
            offer_coin,
            offer_contract,
            offer_ident,
            offer_amount,
            _,
        ) = self._parse_offer_item(offer[0])

        offer_key = item.get('order_hash')
        if self._is_locked(params.get('consideration'), direction, offerer):
            logger.info(f'Locked {direction} skipped: offer_key={offer_key}')
            return None

        price = item.get('price', dict()).get('current')
        if direction == NftOfferDirection.LISTING and price:
            pay_amount = Decimal(price.get('value'))
            pay_contract = None
            pay_ident = None
            pay_coin = OPENSEA_COINS.get(price.get('currency'))
        else:
            pay = self._parse_consideration(params.get('consideration'), offerer)
            pay_coin, pay_contract, pay_ident, pay_amount = next(
                pay, (None, None, None, None)
            )

        return NftOffer.from_api(
            offer_key=offer_key,
            direction=direction,
            collection=collection,
            contract=contract,
            blockchain=self._blockchain,
            offerer=offerer,
            start_time=params.get('startTime'),
            end_time=params.get('endTime'),
            offer_coin=offer_coin,
            offer_contract=offer_contract,
            offer_ident=offer_ident,
            offer_amount=offer_amount,
            pay_coin=pay_coin,
            pay_contract=pay_contract,
            pay_ident=pay_ident,
            pay_amount=pay_amount,
        )

    @staticmethod
    def _is_locked(items: list[dict], direction: NftOfferDirection, offerer: str):
        locks = [t for t in items if t.get('itemType') not in ['0', '1']]
        if direction == NftOfferDirection.LISTING:
            return any(locks)

        locks = [t for t in locks if t.get('recipient').lower() != offerer]
        return any(locks)

    @staticmethod
    def _parse_contract(item) -> Optional[str]:
        criteria = item.get('criteria')
        if not criteria:
            return None

        contract = criteria.get('contract')
        if not contract:
            return None

        if result := contract.get('address'):
            return result.lower()

    @staticmethod
    def _get_offer_params(item):
        if proto := item.get('protocol_data'):
            return proto.get('parameters')

    def _parse_consideration(
        self, items, recipient
    ) -> Iterable[tuple[Optional[Coin], Optional[str], Optional[str], Optional[str]]]:
        if not items:
            return

        for item in items:
            coin, contract, ident, amount, rec = self._parse_offer_item(item)
            if rec == recipient:
                yield coin, contract, ident, amount

    def _parse_offer_item(
        self, param
    ) -> tuple[Optional[Coin], Optional[str], Optional[str], str, Optional[str]]:
        type_ = self._get_type(param.get('itemType'))
        token = param.get('token')
        amount = param.get('startAmount')
        recipient = param.get('recipient')
        if recipient:
            recipient = recipient.lower()

        if type_ in [OfferItemType.NATIVE, OfferItemType.ERC20] and token:
            coin = OPENSEA_CONTRACTS.get((token.lower(), self._blockchain))
            return coin, token, None, amount, recipient

        ident = param.get('identifierOrCriteria')
        if ident == '0':
            ident = None

        return None, token, ident, amount, recipient

    @staticmethod
    def _get_type(item_type) -> Optional[OfferItemType]:
        if not item_type:
            return None

        return OFFER_ITEM_TYPES.get(item_type)

    @staticmethod
    def _coalesce(fetch_results: Iterable[Tuple[FetchResult, Optional[str]]]):
        data = []
        errors = []
        last = None
        last_cursor = None
        for item, cursor in fetch_results:
            last_cursor = cursor
            last = item
            if item.data:
                data.append(item.data)

            if item.errors:
                errors.extend(item.errors)

        if not last:
            return FetchResult(data=data, errors=errors, cursor=last_cursor)

        return FetchResult(
            status_code=last.status_code,
            headers=last.headers,
            data=data,
            errors=errors,
            extra=last.extra,
            cursor=last_cursor,
            time=last.time,
        )

    def _yield_contracts(self, ident: str, contracts: dict) -> Iterable[ContractInfo]:
        if not contracts:
            return

        for item in contracts:
            chain = item.get('chain')
            blockchain = self.opensea_blockchains_map.get(chain)
            address = item.get('address')

            if not blockchain:
                logger.warning(
                    f'Could not map {chain} to known blockchains for collection {ident}'
                )
                continue

            if not address:
                logger.warning(
                    f'No address available for item with chain {chain} for collection {ident}'
                )
                continue

            yield ContractInfo.from_api(blockchain=blockchain, address=address)

    def _should_retry(self, data):
        if not data.errors:
            return False

        retry = bool([t for t in data.errors if 'TOO MANY REQUESTS' in str(t).upper()])
        if retry:
            delay = data.headers.get('retry-after', '60')
            try:
                seconds = int(delay)
            except ValueError:
                seconds = 60

            logger.warning(f'Service unavailable - will retry after {seconds}s sleep')

            self._sleep_provider.sleep(self.base_url, seconds=seconds)
            return True

        return False
