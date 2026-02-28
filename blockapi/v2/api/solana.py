import json
import logging
import os
from typing import Dict, List, Optional, Set

from cytoolz import reduceby
from requests import HTTPError, Response

from blockapi.utils.user_agent import get_random_user_agent
from blockapi.v2.base import (
    ApiException,
    ApiOptions,
    BalanceMixin,
    BlockchainApi,
    CustomizableBlockchainApi,
    InvalidAddressException,
)
from blockapi.v2.coins import COIN_SOL
from blockapi.v2.models import (
    AssetType,
    BalanceItem,
    Blockchain,
    Coin,
    CoinInfo,
    FetchResult,
    ParseResult,
)

logger = logging.getLogger(__name__)

JUP_AG_BAN_LIST_URL = os.getenv(
    'BLOCKAPI_JUP_AG_BAN_LIST_URL',
    'https://raw.githubusercontent.com/jup-ag/token-list/main/banned-tokens.csv',
)


class SolanaApi(CustomizableBlockchainApi, BalanceMixin):
    """
    Solana RPC
    API docs: https://docs.solana.com/apps/jsonrpc-api
    """

    # ── Class configuration ───────────────────────────────────────

    coin = COIN_SOL
    api_options = ApiOptions(
        blockchain=Blockchain.SOLANA,
        base_url='https://api.mainnet-beta.solana.com/',
        start_offset=0,
        max_items_per_page=1000,
        page_offset_step=1,
    )

    # API uses post requests
    supported_requests = {}

    _ban_list: Optional[Set[str]] = None
    _das_cache: Dict[str, Optional[dict]] = {}

    # ── Initialization ────────────────────────────────────────────

    def __init__(self, base_url: Optional[str] = None, include_nfts: bool = False):
        super().__init__(base_url)
        self.include_nfts = include_nfts

    # ── Public interface (BalanceMixin contract) ──────────────────

    def fetch_balances(self, address: str) -> FetchResult:
        das_response = self._fetch_das_assets_by_owner(address)
        raw_staked_sol = self._fetch_staked_sol(address)
        raw_rent_reserve = self._fetch_stake_rent_reserve(raw_staked_sol)

        return FetchResult(
            data=das_response,
            extra=dict(
                raw_staked_sol=raw_staked_sol,
                raw_rent_reserve=raw_rent_reserve,
            ),
        )

    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        raw_staked_sol = fetch_result.extra['raw_staked_sol']
        raw_rent_reserve = fetch_result.extra['raw_rent_reserve']

        das_result = fetch_result.data.get('result', {})
        das_items = das_result.get('items', [])
        native_balance_info = das_result.get('nativeBalance', {})

        balances = []
        if sol_balance := self._get_sol_balance_from_das(native_balance_info):
            balances.append(sol_balance)

        if staked_sol_balance := self._get_staked_sol_balance(raw_staked_sol):
            balances.append(staked_sol_balance)
            balances.append(
                self._get_stake_rent_reserve(staked_sol_balance, raw_rent_reserve)
            )

        token_balances = [
            b
            for item in das_items
            if (b := self._parse_das_token_balance(item)) is not None
        ]
        if token_balances:
            balances.extend(self.merge_balances_with_same_coin(token_balances))

        return ParseResult(data=balances)

    # ── Other public methods ──────────────────────────────────────

    def get_coin(self, fetch_params: tuple[str, int]) -> Coin:
        contract, decimals = fetch_params
        self._fetch_das_assets([contract])

        asset = self._das_cache.get(contract)
        coin = self._build_coin_from_das_asset(asset) if asset else None
        if not coin:
            coin = Coin.from_api(
                blockchain=Blockchain.SOLANA,
                decimals=decimals,
                address=contract,
                standards=['SPL'],
            )

        return coin

    # ── Properties ────────────────────────────────────────────────

    @property
    def ban_list(self) -> set[str]:
        if self._ban_list is None:
            response = self._get_from_url(JUP_AG_BAN_LIST_URL)
            if not response:
                self._ban_list = set()
                return self.ban_list

            ban_list = response.text.strip().split('\n')
            self._ban_list = set(i.split(',')[0] for i in ban_list[1:])
        return self._ban_list

    # ── Private: DAS fetching ─────────────────────────────────────

    def _fetch_das_assets_by_owner(self, address: str) -> dict:
        all_items = []
        native_balance = None
        page = 1
        while True:
            response = self._request(
                'getAssetsByOwner',
                {
                    'ownerAddress': address,
                    'page': page,
                    'limit': 1000,
                    'displayOptions': {
                        'showFungible': True,
                        'showNativeBalance': True,
                    },
                },
            )
            result = response.get('result', {})
            items = result.get('items', [])

            all_items.extend(items)
            if native_balance is None:
                native_balance = result.get('nativeBalance', {})

            if len(items) < 1000:
                break
            page += 1

        return {'result': {'items': all_items, 'nativeBalance': native_balance or {}}}

    def _fetch_das_assets(self, mint_addresses: List[str]) -> None:
        """Batch-fetch token metadata via DAS and populate cache."""
        uncached = [m for m in mint_addresses if m not in self._das_cache]
        if not uncached:
            return

        chunk_size = 1000
        for i in range(0, len(uncached), chunk_size):
            chunk = uncached[i : i + chunk_size]
            try:
                response = self._request(
                    'getAssetBatch',
                    {'ids': chunk, 'options': {'showFungible': True}},
                )
                results = response.get('result', [])
                fetched_ids = set()
                for asset in results:
                    if not asset:
                        continue

                    mint = asset.get('id')
                    if mint:
                        self._das_cache[mint] = asset
                        fetched_ids.add(mint)

                # Mark unfound mints as None so we don't re-fetch
                for mint in chunk:
                    if mint not in fetched_ids:
                        self._das_cache[mint] = None
            except Exception as e:
                logger.warning('DAS getAssetBatch failed: %s', e)

    # ── Private: Staking fetching ─────────────────────────────────

    def _fetch_staked_sol(self, address: str) -> dict:
        return self._request(
            method='getProgramAccounts',
            params=[
                'Stake11111111111111111111111111111111111111',
                {
                    'filters': [
                        {
                            'memcmp': {
                                'offset': 44,
                                'bytes': address,
                                "encoding": 'base58',
                            }
                        }
                    ],
                    'encoding': 'jsonParsed',
                    'dataSlice': None,
                    'commitment': 'finalized',
                    'minContextSlot': None,
                    'withContext': None,
                },
            ],
        )

    def _fetch_stake_rent_reserve(self, raw_staked_sol: dict) -> list[dict]:
        stake_accounts = [r['pubkey'] for r in raw_staked_sol['result']]
        results = []
        for a in stake_accounts:
            results.append(self._request(method='getBalance', params=[a]))

        return results

    # ── Private: Parsing & coin building ──────────────────────────

    def _get_sol_balance_from_das(
        self,
        native_balance_info: dict,
    ) -> Optional[BalanceItem]:
        lamports = native_balance_info.get('lamports', 0)
        if int(lamports) == 0:
            return None

        return BalanceItem.from_api(
            balance_raw=lamports,
            coin=self.coin,
            last_updated=None,
            raw={'nativeBalance': native_balance_info},
        )

    def _parse_das_token_balance(self, item: dict) -> Optional[BalanceItem]:
        token_info = item.get('token_info', {})
        balance_raw = token_info.get('balance', 0)
        if int(balance_raw) == 0:
            return None

        mint_address = item.get('id', '')
        if mint_address in self.ban_list:
            return None

        coin = self._build_coin_from_das_asset(item)
        if not coin:
            coin = Coin.from_api(
                blockchain=Blockchain.SOLANA,
                decimals=token_info.get('decimals', 0),
                address=mint_address,
                standards=['SPL'],
            )

        if coin.is_nft and not self.include_nfts:
            return None

        asset_type = AssetType.NFT if coin.is_nft else AssetType.AVAILABLE

        return BalanceItem.from_api(
            balance_raw=balance_raw,
            coin=coin,
            asset_type=asset_type,
            raw=item,
        )

    def _build_coin_from_das_asset(self, asset: dict) -> Optional[Coin]:
        content = asset.get('content', {})
        metadata = content.get('metadata', {})
        token_info = asset.get('token_info', {})
        links = content.get('links', {})

        symbol = metadata.get('symbol') or token_info.get('symbol')
        if not symbol:
            return None

        standards = ['SPL']
        interface = asset.get('interface', '')
        if interface:
            standards.append(interface)

        return Coin(
            symbol=symbol,
            name=metadata.get('name', ''),
            decimals=token_info.get('decimals', 0),
            blockchain=Blockchain.SOLANA,
            address=asset.get('id', ''),
            standards=standards,
            info=CoinInfo.from_api(
                logo_url=links.get('image'),
                tags=metadata.get('attributes'),
            ),
        )

    def _get_staked_sol_balance(self, response: dict) -> Optional[BalanceItem]:
        if not response['result']:
            return

        balance_raw = sum(
            int(r['account']['data']['parsed']['info']['stake']['delegation']['stake'])
            for r in response['result']
        )

        return BalanceItem.from_api(
            balance_raw=balance_raw,
            coin=self.coin,
            asset_type=AssetType.STAKED,
            raw=response['result'],
        )

    def _get_stake_rent_reserve(
        self, staked_sol: BalanceItem, responses: list[dict]
    ) -> BalanceItem:
        total_raw = sum(r['result']['value'] for r in responses)
        available_raw = total_raw - int(staked_sol.balance_raw)

        return BalanceItem.from_api(
            balance_raw=available_raw,
            coin=self.coin,
            asset_type=AssetType.LOCKED,
            raw=responses,
        )

    # ── Static methods ────────────────────────────────────────────

    @staticmethod
    def merge_balances_with_same_coin(
        token_balances: list[BalanceItem],
    ) -> list[BalanceItem]:
        return list(
            reduceby(
                key=lambda b: b.coin.address if b.coin else b.coin_contract.contract,
                binop=lambda v1, v2: v1 + v2,
                seq=token_balances,
            ).values()
        )

    # ── Infrastructure ────────────────────────────────────────────

    def _request(self, method, params):
        body = json.dumps(
            {'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}
        )
        return self.post(body=body, headers={'Content-Type': 'application/json'})

    def _get_from_url(self, url: str):
        try:
            response = self._session.get(url)
            response.raise_for_status()
        except HTTPError as e:
            logger.error(e)
            return

        return response

    # ── Base class overrides ──────────────────────────────────────

    def _opt_raise_on_other_error(self, response: Response) -> None:
        json_response = response.json()
        if 'error' not in json_response:
            return

        if 'Invalid param' in json_response['error']['message']:
            raise InvalidAddressException(f'Invalid address format.')
        else:
            raise ApiException(json_response['error']['message'])


class SolscanApi(BlockchainApi):
    coin = COIN_SOL
    api_options = ApiOptions(
        blockchain=Blockchain.SOLANA,
        base_url='https://api.solscan.io/',
        start_offset=0,
        max_items_per_page=1000,
        page_offset_step=1,
    )

    supported_requests = {'get_stake_balances': 'account/stake?address={address}'}

    def get_staked_balance(self, address: str) -> Optional[BalanceItem]:
        response = self.get(
            'get_stake_balances',
            headers={'User-Agent': get_random_user_agent()},
            address=address,
        )
        if not response['data']:
            return

        # return only delegated or all types?
        balance_raw = sum(int(i['amount']) for i in response['data'].values())

        return BalanceItem.from_api(
            balance_raw=balance_raw,
            coin=self.coin,
            asset_type=AssetType.STAKED,
            last_updated=None,
            raw=response['data'],
        )
