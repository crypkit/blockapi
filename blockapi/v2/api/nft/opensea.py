import logging
from enum import Enum
from typing import Iterable, Optional

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
    FetchResult,
    NftCollectionStats,
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


class OpenSeaApi(BlockchainApi, INftProvider, INftParser):
    """
    Ethereum
    API docs: https://docs.opensea.io/reference/api-overview
    Explorer: https://opensea.io/
    """

    supported_blockchains = {
        Blockchain.ETHEREUM: 'ethereum',
        Blockchain.POLYGON: 'matic',
        Blockchain.KLAYTN_CYPRESS: 'klaytn',
        Blockchain.BINANCE_SMART_CHAIN: 'bsc',
        Blockchain.ARBITRUM: 'arbitrum',
        Blockchain.ARBITRUM_NOVA: 'arbitrum_nova',
        Blockchain.AVALANCHE: 'avalanche',
        Blockchain.OPTIMISM: 'optimism',
        Blockchain.SOLANA: 'solana',
        Blockchain.BASE: 'base',
        Blockchain.ZORA: 'zora',
    }

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
    ):
        super().__init__(api_key)

        self._blockchain = blockchain
        self._opensea_chain = self.supported_blockchains.get(blockchain)
        if not self._opensea_chain:
            raise ApiException(f"Blockchain '{blockchain.value}' is not supported")

        self._headers = {'accept': 'application/json', 'x-api-key': api_key}
        self._sleep_provider = sleep_provider or SleepProvider()

    def fetch_nfts(self, address: str) -> FetchResult:
        logger.info(f'Fetch nfts from {address}')
        return self._coallesce(self._yield_nfts(address))

    def parse_nfts(self, fetch_result: FetchResult) -> ParseResult:
        logger.info(f'Parse nfts')

        if not fetch_result:
            return ParseResult()

        parsed = list(self._yield_parsed_nfts(fetch_result.data))
        return ParseResult(data=parsed, errors=fetch_result.errors)

    def fetch_offers(self, collection: str) -> FetchResult:
        return self.get_data(
            'get_offers',
            headers=self._headers,
            collection=collection,
            chain=self._opensea_chain,
            extra=dict(collection=collection),
        )

    def parse_offers(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result or not fetch_result.data:
            return ParseResult()

        return ParseResult(
            data=list(
                self._yield_offers(
                    NftOfferDirection.OFFER,
                    fetch_result.extra,
                    fetch_result.data.get('offers'),
                )
            )
        )

    def fetch_listings(self, collection: str) -> FetchResult:
        return self.get_data(
            'get_listings',
            headers=self._headers,
            collection=collection,
            chain=self._opensea_chain,
            extra=dict(collection=collection),
        )

    def parse_listings(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result or not fetch_result.data:
            return ParseResult()

        return ParseResult(
            data=list(
                self._yield_offers(
                    NftOfferDirection.LISTING,
                    fetch_result.extra,
                    fetch_result.data.get('listings'),
                )
            )
        )

    def fetch_collection_stats(self, collection: str) -> FetchResult:
        return self.get_data(
            'get_collection_stats',
            headers=self._headers,
            collection=collection,
            chain=self._opensea_chain,
        )

    def parse_collection_stats(self, fetch_result: FetchResult) -> ParseResult:
        parsed, error = self._parse_collection(fetch_result.data.get('total'))

        return ParseResult(
            data=[parsed] if parsed else None, errors=[error] if error else None
        )

    def _yield_nfts(self, address: str) -> Iterable[FetchResult]:
        fetched = self._fetch_nfts_page(address)
        cursor = fetched.data.get('next')
        cursors = {cursor}
        yield fetched

        while cursor:
            try:
                self._sleep_provider.sleep(self.base_url, self.api_options.rate_limit)
                fetched = self._fetch_nfts_page(address, cursor)
                cursor = fetched.data.get('next')
                yield fetched

                if cursor in cursors:
                    logger.warning(
                        f'Detected duplicate cursor {cursor} while fetching NFTs for {address}'
                    )
                    break

                cursors.add(cursor)
            except Exception as e:
                logger.error(f'Error fetching {address} NFTs from OpenSea')
                logger.exception(e)
                break

    def _fetch_nfts_page(
        self, address: str, cursor: Optional[str] = None
    ) -> FetchResult:
        params = dict(next=cursor) if cursor else dict()
        return self.get_data(
            'get_nfts',
            headers=self._headers,
            params=params,
            address=address,
            chain=self._opensea_chain,
        )

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
                    image_url=item.get('image_url'),
                    metadata_url=item.get('metadata_url'),
                    created_time=item.get('created_at'),
                    updated_time=item.get('updated_at'),
                    is_disabled=item.get('is_disabled'),
                    is_nsfw=item.get('is_nsfw'),
                    blockchain=self._blockchain,
                    asset_type=AssetType.AVAILABLE,
                )

    @staticmethod
    def _parse_collection(
        data: dict,
    ) -> tuple[Optional[NftCollectionStats], Optional[str]]:
        symbol = data.get('floor_price_symbol')
        coin = OPENSEA_COINS.get(symbol)
        if not coin:
            if not symbol:
                return None, None

            return None, f'There is no mapping for opensea symbol {symbol}'

        stats = NftCollectionStats.from_api(
            coin=coin,
            volume=data.get('volume'),
            market_cap=data.get('market_cap'),
            floor_price=data.get('floor_price'),
            average_price=data.get('average_price'),
            sales_count=data.get('sales'),
            owners_count=data.get('num_owners'),
        )

        return stats, None

    def _yield_offers(
        self, direction: NftOfferDirection, extra: dict, items: list
    ) -> Iterable[NftOffer]:
        collection = extra.get('collection')
        contract = extra.get('contract')

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
        pay = self._parse_consideration(params.get('consideration'), offerer)
        pay_coin, pay_contract, pay_ident, pay_amount = next(
            pay, (None, None, None, None)
        )

        return NftOffer.from_api(
            direction=direction,
            collection=collection,
            contract=contract,
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

    def _coallesce(self, fetch_results: Iterable[FetchResult]):
        data = []
        errors = []
        last = None
        for item in fetch_results:
            last = item
            if item.data:
                data.append(item.data)

            if item.errors:
                errors.extend(item.errors)

        if not last:
            return FetchResult(data=data, errors=errors)

        return FetchResult(
            status_code=last.status_code,
            headers=last.headers,
            extra=last.extra,
            time=last.time,
            data=data,
            errors=errors,
        )
