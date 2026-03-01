import json
import logging
import os
from typing import Optional, Union

from cytoolz import reduceby
from requests import Response
from requests.exceptions import RequestException

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
    NFT_STANDARDS,
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
    """Solana JSON-RPC client with DAS metadata integration.

    API docs: https://docs.solana.com/apps/jsonrpc-api

    Caching architecture
    --------------------
    ``_das_cache`` and ``_ban_list`` are **class-level** attributes shared
    across all instances.  This is intentional: DAS metadata and the Jupiter
    ban list are global and rarely change. Sharing them avoids redundant RPC/HTTP calls
    when multiple ``SolanaApi`` instances coexist (e.g. one per user request
    in a web service).
    """

    # ── Configuration ──────────────────────────────────────────

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

    TOKEN_PROGRAM_ID = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
    TOKEN_2022_PROGRAM_ID = 'TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb'
    STAKE_PROGRAM_ID = 'Stake11111111111111111111111111111111111111'
    STAKE_AUTHORITY_OFFSET = 44
    DAS_BATCH_SIZE = 1000
    _JSONRPC_INVALID_PARAMS = -32602

    # Class-level cache: shared across instances to avoid redundant DAS RPCs.
    _das_cache: dict[str, dict] = {}

    # Class-level ban list: shared across instances
    _ban_list: set = set()

    # ── Initialization ─────────────────────────────────────────

    def __init__(self, base_url: Optional[str] = None, include_nfts: bool = False):
        super().__init__(base_url)
        self.include_nfts = include_nfts
        self._request_id = 0

    # ── Balance API ────────────────────────────────────────────

    def fetch_balances(self, address: str) -> FetchResult:
        """Fetch native SOL, token accounts, DAS metadata, and staking data."""
        sol_response = self._request('getBalance', [address])

        raw_token_balances = self._request(
            'getTokenAccountsByOwner',
            [
                address,
                {'programId': self.TOKEN_PROGRAM_ID},
                {'encoding': 'jsonParsed'},
            ],
        )
        raw_token2022_balances = self._request(
            'getTokenAccountsByOwner',
            [
                address,
                {'programId': self.TOKEN_2022_PROGRAM_ID},
                {'encoding': 'jsonParsed'},
            ],
        )

        mint_addresses = self._collect_mint_addresses(
            raw_token_balances, raw_token2022_balances
        )
        self._fetch_das_assets(mint_addresses)

        raw_staked_sol = self._fetch_staked_sol(address)
        raw_rent_reserve = self._fetch_stake_account_balances(raw_staked_sol)

        return FetchResult(
            data=sol_response,
            extra=dict(
                raw_token_balances=raw_token_balances,
                raw_token2022_balances=raw_token2022_balances,
                raw_staked_sol=raw_staked_sol,
                raw_rent_reserve=raw_rent_reserve,
            ),
        )

    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        """Parse fetched data into a list of BalanceItems."""
        raw_staked_sol = fetch_result.extra['raw_staked_sol']
        raw_rent_reserve = fetch_result.extra['raw_rent_reserve']

        balances = []

        if sol_balance := self._parse_sol_balance(fetch_result.data):
            balances.append(sol_balance)

        if staked_sol_balance := self._parse_staked_balance(raw_staked_sol):
            balances.append(staked_sol_balance)
            balances.append(
                self._parse_rent_reserve(staked_sol_balance, raw_rent_reserve)
            )

        all_raw_tokens = (
            fetch_result.extra['raw_token_balances']['result']['value']
            + fetch_result.extra['raw_token2022_balances']['result']['value']
        )
        token_balances = [
            b
            for raw in all_raw_tokens
            if (b := self._parse_token_balance(raw)) is not None
        ]

        if token_balances:
            balances.extend(self.merge_balances_with_same_coin(token_balances))

        return ParseResult(data=balances)

    def get_coin(self, fetch_params: tuple[str, int]) -> Coin:
        """Fetch and build a Coin for a given contract address and decimals."""
        contract, decimals = fetch_params
        self._fetch_das_assets([contract])
        return self._resolve_coin(contract, decimals)

    @property
    def ban_list(self) -> set[str]:
        """Return the set of banned token mints from Jupiter."""
        if not self._ban_list:
            if response := self._get_from_url(JUP_AG_BAN_LIST_URL):
                ban_list = response.text.strip().split('\n')
                SolanaApi._ban_list = set(i.split(',')[0] for i in ban_list[1:])
        return self._ban_list

    @staticmethod
    def merge_balances_with_same_coin(
        token_balances: list[BalanceItem],
    ) -> list[BalanceItem]:
        """Merge token balances that share the same coin address."""
        return list(
            reduceby(
                key=lambda b: b.coin.address if b.coin else b.coin_contract.contract,
                binop=lambda v1, v2: v1 + v2,
                seq=token_balances,
            ).values()
        )

    # ── Token processing ───────────────────────────────────────

    def _collect_mint_addresses(self, *token_responses: dict) -> list[str]:
        """Collect mint addresses from token account responses."""
        mints = []
        for response in token_responses:
            for account in response.get('result', {}).get('value', []):
                info = self._extract_token_info(account)
                amount = int(info.get('tokenAmount', {}).get('amount', 0))
                mint = info.get('mint')
                if amount > 0 and mint:
                    mints.append(mint)
        return mints

    def _resolve_coin(self, mint: str, decimals: int) -> Coin:
        """Resolve a Coin for a mint address, trying DAS cache first."""
        if das_asset := self._das_cache.get(mint):
            if coin := self._build_coin_from_das_asset(das_asset):
                return coin

        return Coin.from_api(
            blockchain=Blockchain.SOLANA,
            decimals=decimals,
            address=mint,
            standards=['SPL'],
        )

    def _parse_token_balance(self, raw: dict) -> Optional[BalanceItem]:
        """Parse a single token account into a BalanceItem."""
        info = self._extract_token_info(raw)
        token_amount = info.get('tokenAmount', {})
        balance_raw = int(token_amount.get('amount', 0))
        if balance_raw == 0:
            return None

        mint = info.get('mint')
        if mint in self.ban_list:
            return None

        decimals = int(token_amount.get('decimals', 0))
        coin = self._resolve_coin(mint, decimals)

        if coin.is_nft and not self.include_nfts:
            return None

        asset_type = AssetType.NFT if coin.is_nft else AssetType.AVAILABLE

        return BalanceItem.from_api(
            balance_raw=balance_raw,
            coin=coin,
            asset_type=asset_type,
            raw=raw,
        )

    @staticmethod
    def _extract_token_info(account: dict) -> dict:
        """Extract parsed token info from an account response."""
        return (
            account.get('account', {}).get('data', {}).get('parsed', {}).get('info', {})
        )

    # ── DAS integration ────────────────────────────────────────

    def _fetch_das_assets(self, mint_addresses: list[str]) -> None:
        """Batch-fetch token metadata via DAS and populate cache."""
        uncached = [m for m in mint_addresses if m not in self._das_cache]
        if not uncached:
            return

        for i in range(0, len(uncached), self.DAS_BATCH_SIZE):
            chunk = uncached[i : i + self.DAS_BATCH_SIZE]
            try:
                response = self._request(
                    'getAssetBatch',
                    {'ids': chunk, 'options': {'showFungible': True}},
                )
            except (ApiException, RequestException) as e:
                logger.warning('DAS getAssetBatch failed: %s', e)
                continue

            results = response.get('result', [])
            for asset in results:
                if asset is None:
                    continue
                if mint := asset.get('id'):
                    self._das_cache[mint] = asset

    def _build_coin_from_das_asset(self, asset: dict) -> Optional[Coin]:
        """Build a Coin from a DAS asset response."""
        content = asset.get('content', {})
        metadata = content.get('metadata', {})
        token_info = asset.get('token_info', {})
        links = content.get('links', {})

        symbol = metadata.get('symbol') or token_info.get('symbol')

        standards = ['SPL']
        if interface := asset.get('interface'):
            standards.append(interface)

        # Detect NFTs with non-standard DAS interface (e.g. "Custom"):
        # decimals=0 + supply=1 is the universal Solana NFT signature.
        if interface not in NFT_STANDARDS:
            supply = token_info.get('supply')
            decimals = token_info.get('decimals')
            if decimals == 0 and supply == 1:
                standards.append('V1_NFT')

        return Coin(
            symbol=symbol,
            name=metadata.get('name') or 'Unknown',
            decimals=token_info.get('decimals', 0),
            blockchain=Blockchain.SOLANA,
            address=asset.get('id'),
            standards=standards,
            info=CoinInfo.from_api(
                logo_url=links.get('image'),
                tags=metadata.get('attributes'),
            ),
        )

    # ── Staking ────────────────────────────────────────────────

    def _fetch_staked_sol(self, address: str) -> dict:
        """Fetch staked SOL accounts for a given address."""
        return self._request(
            method='getProgramAccounts',
            params=[
                self.STAKE_PROGRAM_ID,
                {
                    'filters': [
                        {
                            'memcmp': {
                                'offset': self.STAKE_AUTHORITY_OFFSET,
                                'bytes': address,
                                'encoding': 'base58',
                            }
                        }
                    ],
                    'encoding': 'jsonParsed',
                    'commitment': 'finalized',
                },
            ],
        )

    def _fetch_stake_account_balances(self, raw_staked_sol: dict) -> dict:
        """Fetch balances for all stake accounts in a single RPC call."""
        stake_accounts = [r['pubkey'] for r in raw_staked_sol.get('result', [])]
        if not stake_accounts:
            return {'result': {'value': []}}
        return self._request(
            method='getMultipleAccounts',
            params=[stake_accounts],
        )

    # ── Balance parsing ────────────────────────────────────────

    def _parse_sol_balance(self, response: dict) -> Optional[BalanceItem]:
        """Parse native SOL balance from an RPC response."""
        lamports = response.get('result', {}).get('value', 0)
        if int(lamports) == 0:
            return None

        return BalanceItem.from_api(
            balance_raw=lamports,
            coin=self.coin,
            last_updated=None,
            raw=response,
        )

    def _parse_staked_balance(self, response: dict) -> Optional[BalanceItem]:
        """Parse total staked SOL balance from stake accounts."""
        if not response.get('result'):
            return None

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

    def _parse_rent_reserve(
        self, staked_sol: BalanceItem, response: dict
    ) -> BalanceItem:
        """Parse rent reserve balance from getMultipleAccounts response."""
        accounts = response.get('result', {}).get('value', [])
        total_raw = sum(a.get('lamports', 0) for a in accounts if a is not None)
        available_raw = total_raw - int(staked_sol.balance_raw)

        return BalanceItem.from_api(
            balance_raw=available_raw,
            coin=self.coin,
            asset_type=AssetType.LOCKED,
            raw=response,
        )

    # ── Infrastructure ─────────────────────────────────────────

    def _request(self, method: str, params: Union[list, dict]) -> dict:
        """Send a JSON-RPC request to the Solana RPC endpoint."""
        self._request_id += 1
        body = json.dumps(
            {
                'jsonrpc': '2.0',
                'id': self._request_id,
                'method': method,
                'params': params,
            }
        )
        return self.post(body=body, headers={'Content-Type': 'application/json'})

    def _get_from_url(self, url: str) -> Optional[Response]:
        """Perform a GET request to an external URL."""
        try:
            response = self._session.get(url)
            response.raise_for_status()
        except RequestException as e:
            logger.error(e)
            return None

        return response

    def _opt_raise_on_other_error(self, response: Response) -> None:
        """Raise ApiException or InvalidAddressException on RPC errors."""
        json_response = response.json()
        if 'error' not in json_response:
            return

        error = json_response['error']
        message = error.get('message', '')

        if (
            error.get('code') == self._JSONRPC_INVALID_PARAMS
            or 'Invalid param' in message
        ):
            raise InvalidAddressException('Invalid address format.')
        else:
            raise ApiException(message)


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

        balance_raw = sum(int(i['amount']) for i in response['data'].values())

        return BalanceItem.from_api(
            balance_raw=balance_raw,
            coin=self.coin,
            asset_type=AssetType.STAKED,
            last_updated=None,
            raw=response['data'],
        )
