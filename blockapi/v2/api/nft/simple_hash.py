import logging
from typing import Iterable, Optional

from blockapi.v2.base import BlockchainApi, INftParser, INftProvider, ISleepProvider
from blockapi.v2.coins import COIN_BTC, COIN_ETH, COIN_SOL
from blockapi.v2.models import (
    ApiOptions,
    AssetType,
    Blockchain,
    Coin,
    ContractInfo,
    FetchResult,
    NftCollection,
    NftOffer,
    NftOfferDirection,
    NftPrice,
    NftToken,
    NftVolumes,
    ParseResult,
)

logger = logging.getLogger(__name__)

SIMPLE_HASH_COINS = {
    'bitcoin.native': COIN_BTC,
    'solana.native': COIN_SOL,
    'ethereum.native': COIN_ETH,
}


class SimpleHashApi(BlockchainApi, INftProvider, INftParser):
    """
    API docs: https://docs.simplehash.com/reference/overview
    Explorer: https://magiceden.io/
    """

    default_blockchain = NotImplemented
    default_collection = NotImplemented

    api_options = ApiOptions(
        blockchain=NotImplemented,
        base_url='https://api.simplehash.com/api/v0/nfts/',
        rate_limit=0.01,  # 100 per second for free account
    )

    supported_requests = {
        'get_nfts': 'owners?chains={chain}&wallet_addresses={address}',
        'get_collection': 'collections/ids?collection_ids={slug}',
        'get_collection_activity': 'collections_activity?collection_ids={slug}',
        'get_bids': 'bids/collection/{slug}',
        'get_listings': 'listings/collection/{slug}',
        'get_wallet_bids': 'bids/wallets?chains={chain}&wallet_addresses={address}',
        'get_wallet_listings': 'listings/wallets?chains={chain}&wallet_addresses={address}'
        '&include_nft_details={include_nft_details}',
    }

    def __init__(self, blockchain, simplehash_blockchain, api_key, sleep_provider):
        super().__init__(sleep_provider=sleep_provider)

        self._api_key = api_key
        self.headers = {'accept': 'application/json', 'X-API-KEY': api_key}
        self.api_options.blockchain = blockchain
        self._blockchain = blockchain
        self._simplehash_blockchain = simplehash_blockchain

    def fetch_nfts(self, address: str, cursor: Optional[str] = None) -> FetchResult:
        return self.get_data(
            'get_nfts',
            headers=self.headers,
            params=dict(cursor=cursor) if cursor else None,
            chain=self._simplehash_blockchain,
            address=address,
            extra=dict(address=address),
        )

    def parse_nfts(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result or not fetch_result.data:
            return ParseResult(errors=fetch_result.errors if fetch_result else None)

        parsed = list(
            self._yield_parsed_nfts(
                fetch_result.data, address=fetch_result.extra.get('address')
            )
        )
        return ParseResult(
            data=parsed,
            errors=fetch_result.errors,
            cursor=fetch_result.data.get('next_cursor'),
        )

    def _yield_parsed_nfts(self, data, address):
        yield from self._yield_parsed_nfts_from_tokens(
            self._yield_tokens(data.get('listings')), address
        )
        yield from self._yield_parsed_nfts_from_tokens(data.get('nfts'), address)

    @staticmethod
    def _yield_tokens(items):
        if not items:
            return

        for item in items:
            if nft := item.get('nft_details'):
                yield nft

    def _yield_parsed_nfts_from_tokens(self, items, address):
        if not items:
            return

        for item in items:
            collection = item.get('collection')
            contract = item.get('contract')
            ident = item.get('nft_id')

            if not ident:
                continue

            collection_id = collection.get('collection_id') or self.default_collection
            standard = contract.get('type', 'ordinals').lower()

            yield NftToken.from_api(
                ident=ident,
                collection=collection_id,
                contract=collection_id,
                standard=standard,
                name=item.get('name') or contract.get('name'),
                description=None,
                amount=self._get_amount(item.get('owners'), address),
                image_url=item.get('image_url'),
                metadata_url=None,
                updated_time=item.get('created_date'),
                is_disabled=False,
                is_nsfw=False,
                blockchain=self._blockchain,
                asset_type=AssetType.AVAILABLE,
                market_url=self._get_market_url(collection),
            )

    @staticmethod
    def _get_market_url(collection):
        eden = None
        if pages := collection.get('marketplace_pages'):
            for page in pages:
                marketplace = page.get('marketplace_id')
                if marketplace == 'magiceden':
                    eden = page.get('nft_url')

                if marketplace == 'opensea':
                    return page.get('nft_url')

        return eden

    @staticmethod
    def _get_amount(owners, address):
        if not owners:
            return 1

        low_address = address.lower()

        for t in owners:
            if adr := t.get('owner_address'):
                if adr.lower() == low_address:
                    return t.get('quantity')

        return 1

    def fetch_collection(self, collection: str) -> FetchResult:
        collections = self.get_data(
            'get_collection',
            headers=self.headers,
            slug=collection,
        )

        activity = self.get_data(
            'get_collection_activity', headers=self.headers, slug=collection
        )

        return FetchResult.from_fetch_results(
            collections=collections, activity=activity
        )

    def parse_collection(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result or fetch_result.errors:
            return ParseResult(errors=fetch_result.errors if fetch_result else None)

        return ParseResult(
            data=list(self._yield_parsed_collection(fetch_result)),
            errors=fetch_result.errors,
        )

    def _yield_parsed_collection(
        self, fetch_result: FetchResult
    ) -> Iterable[NftCollection]:
        collections = {
            t['collection_id']: t
            for t in fetch_result.data['collections'].get('collections') or []
        }
        activities = {
            t['collection_id']: t
            for t in fetch_result.data['activity'].get('collections') or []
        }

        for key, collection in collections.items():
            activity = activities.get(key)

            ident = collection.get('collection_id')
            yield NftCollection.from_api(
                ident=ident,
                name=collection.get('name')
                or activity.get('name')
                or f'Collection {ident}',
                contracts=[
                    ContractInfo.from_api(
                        blockchain=self._blockchain,
                        address=collection.get('collection_id'),
                    )
                ],
                image=collection.get('image_url'),
                is_disabled=False,
                is_nsfw=False,
                blockchain=self._blockchain,
                floor_prices=self.get_prices(collection.get('floor_prices')),
                best_offers=self.get_prices(collection.get('top_bids')),
                volumes=self._get_volumes(activity),
            )

    def _get_volumes(self, activity) -> NftVolumes:
        if not activity:
            return NftVolumes.from_api(
                coin=self.coin,
            )

        token = activity.get('payment_token') or dict()
        if coin := self._get_coin(token):
            return NftVolumes.from_api(
                coin=coin,
                market_cap_raw=activity.get('market_cap'),
                volume_raw=activity.get('all_time_volume'),
                volume_1d_raw=activity.get('1_day_volume'),
                volume_7d_raw=activity.get('7_day_volume'),
                volume_30d_raw=activity.get('30_day_volume'),
            )

        return NftVolumes.from_api(
            coin=self.coin,
        )

    def get_prices(self, items):
        if not items:
            return dict()

        result = dict()
        for item in items:
            marketplace_id = item.get('marketplace_id')
            amount = item.get('value')
            token = item.get('payment_token')
            if coin := self._get_coin(token):
                result[marketplace_id] = NftPrice.from_api(coin=coin, amount_raw=amount)

        return result if result else None

    def _get_coin(self, token: Optional[dict]) -> Optional[Coin]:
        if not token:
            return None

        if token_id := token.get('payment_token_id'):
            if coin := SIMPLE_HASH_COINS.get(token_id):
                return coin

        return Coin.from_api(
            blockchain=self._blockchain,
            decimals=token.get('decimals'),
            symbol=token.get('symbol'),
            name=token.get('name'),
            address=token.get('address'),
        )

    def fetch_offers(
        self, collection: str, cursor: Optional[str] = None
    ) -> FetchResult:
        return self.get_data(
            'get_bids',
            headers=self.headers,
            params=dict(cursor=cursor) if cursor else None,
            slug=collection,
        )

    def fetch_wallet_offers(
        self, address: str, cursor: Optional[str] = None
    ) -> FetchResult:
        return self.get_data(
            'get_wallet_bids',
            headers=self.headers,
            params=dict(cursor=cursor) if cursor else None,
            chain=self._simplehash_blockchain,
            address=address,
        )

    def parse_wallet_offers(self, fetch_result: FetchResult) -> ParseResult:
        return self.parse_offers(fetch_result)

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
            if item.get('is_private') == 'true':
                continue

            token = item.get('payment_token')
            if coin := self._get_coin(token):
                yield NftOffer.from_api(
                    offer_key=item.get('id'),
                    direction=NftOfferDirection.OFFER,
                    collection=item.get('collection_id'),
                    contract=item.get('collection_id'),
                    blockchain=self._blockchain,
                    offerer=item.get('bidder_address'),
                    start_time=item.get('timestamp'),
                    end_time=item.get('expiration_timestamp'),
                    offer_coin=coin,
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

    def fetch_wallet_listings(
        self, address: str, cursor: Optional[str] = None
    ) -> FetchResult:
        return self.get_data(
            'get_wallet_listings',
            headers=self.headers,
            params=dict(cursor=cursor) if cursor else None,
            chain=self._simplehash_blockchain,
            include_nft_details=0,
            address=address,
        )

    def parse_wallet_listings(self, fetch_result: FetchResult) -> ParseResult:
        return self.parse_listings(fetch_result)

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
            if item.get('is_private') == 'true':
                continue

            token = item.get('payment_token')
            if coin := self._get_coin(token):
                yield NftOffer.from_api(
                    offer_key=item.get('id'),
                    direction=NftOfferDirection.LISTING,
                    collection=item.get('collection_id'),
                    contract=item.get('collection_id'),
                    blockchain=self._blockchain,
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
                    pay_coin=coin,
                )


class SimpleHashBitcoinApi(SimpleHashApi):
    coin = COIN_BTC
    default_blockchain = Blockchain.BITCOIN
    default_collection = 'inscriptions'

    def __init__(self, api_key: str, sleep_provider: ISleepProvider):
        super().__init__(self.default_blockchain, 'bitcoin', api_key, sleep_provider)

    def fetch_collection(self, collection: str) -> FetchResult:
        if collection == self.default_collection:
            return FetchResult.from_dict(
                collections=dict(
                    collections=[
                        dict(
                            collection_id=self.default_collection,
                            name='Inscriptions',
                        )
                    ]
                ),
                activity=dict(),
            )

        return super().fetch_collection(collection)


class SimpleHashSolanaApi(SimpleHashApi):
    coin = COIN_SOL
    default_blockchain = Blockchain.SOLANA

    def __init__(self, api_key: str, sleep_provider: ISleepProvider):
        super().__init__(self.default_blockchain, 'solana', api_key, sleep_provider)

    def fetch_nfts(self, address: str, cursor: Optional[str] = None) -> FetchResult:
        token_cursor = None
        listing_cursor = None
        if cursor:
            target, crs = cursor.split(':')
            if target == 'token':
                token_cursor = crs
            elif target == 'listing':
                listing_cursor = crs

        listings = None
        if not token_cursor:
            listings = self.get_data(
                'get_wallet_listings',
                headers=self.headers,
                params=dict(cursor=listing_cursor) if listing_cursor else None,
                chain=self._simplehash_blockchain,
                include_nft_details=1,
                address=address,
                extra=dict(address=address),
            )

            if self._update_cursor(listings, 'listing'):
                return listings

        data = self.get_data(
            'get_nfts',
            headers=self.headers,
            params=dict(cursor=token_cursor) if token_cursor else None,
            chain=self._simplehash_blockchain,
            address=address,
            extra=dict(address=address),
        )

        self._update_cursor(data, 'token')
        return self._coallesce(listings, data)

    @staticmethod
    def _update_cursor(data, prefix):
        if not data.data:
            return False

        if crs := data.data.get('next_cursor'):
            data.data['next_cursor'] = f'{prefix}:{crs}'
            return True

        return False

    def _coallesce(self, listings, data):
        if data and data.errors:
            return data

        if listings and listings.errors:
            return listings

        if not data or not data.data:
            return listings

        if not listings or not listings.data:
            return data

        data.data['listings'] = listings.data.get('listings', [])
        return data


class SimpleHashEthereumApi(SimpleHashApi):
    coin = COIN_ETH
    default_blockchain = Blockchain.ETHEREUM

    supported_blockchains_map = {
        Blockchain.ARBITRUM: 'arbitrum',
        Blockchain.ARBITRUM_NOVA: 'arbitrum-nova',
        Blockchain.AVALANCHE: 'avalanche',
        Blockchain.BASE: 'base',
        Blockchain.BINANCE_SMART_CHAIN: 'bsc',
        Blockchain.CELO: 'celo',
        Blockchain.ETHEREUM: 'ethereum',
        Blockchain.FANTOM: 'fantom',
        Blockchain.OPTIMISM: 'optimism',
        Blockchain.POLYGON_ZK_EVM: 'polygon-zkevm',
        Blockchain.TEZOS: 'tezos',
        Blockchain.ZORA: 'zora',
    }

    simplehash_blockchains_map = {n: b for b, n in supported_blockchains_map.items()}
    supported_blockchains = list(supported_blockchains_map.keys())

    def __init__(
        self, blockchain: Blockchain, api_key: str, sleep_provider: ISleepProvider
    ):
        chain = self.supported_blockchains_map.get(blockchain)
        if not chain:
            raise Exception(f'Blockchain not supported {blockchain}')

        super().__init__(blockchain, chain, api_key, sleep_provider)
