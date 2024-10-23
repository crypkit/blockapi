import base64
import json
import logging
from typing import Dict, Iterable, Optional, Set

import requests
from cytoolz import reduceby
from requests import Response
from solders.pubkey import Pubkey

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

SOL_TOKEN_LIST_URL = 'https://token-list-api.solana.cloud/v1/list'
JUP_AG_TOKEN_LIST_URL = (
    'https://raw.githubusercontent.com/jup-ag/token-list/main/validated-tokens.csv'
)
JUP_AG_BAN_LIST_URL = (
    'https://raw.githubusercontent.com/jup-ag/token-list/main/banned-tokens.csv'
)
SONAR_TOKEN_LIST_URL = 'https://lively-pine-1ccc.swob.workers.dev/solana'


class SolanaApi(CustomizableBlockchainApi, BalanceMixin):
    """
    Solana RPC
    API docs: https://docs.solana.com/apps/jsonrpc-api
    """

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

    token_program_id = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
    token2022_program_id = 'TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb'
    METADATA_PROGRAM_ID = Pubkey.from_string(
        "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
    )

    _tokens_map: Optional[Dict[str, Dict]] = None
    _ban_list: Optional[Set[str]] = None

    def __init__(self, base_url: Optional[str] = None, fetch_metaplex: bool = True):
        super().__init__(base_url)
        self.fetch_metaplex = fetch_metaplex

    @property
    def tokens_map(self) -> Dict[str, Dict]:
        if self._tokens_map is None:
            map_jup_ag = self._get_token_map_jup_ag()
            map_solana = self._get_token_map_solana()
            self._tokens_map = {**map_jup_ag, **map_solana}

        return self._tokens_map

    def _get_token_map_solana(self) -> Dict[str, Dict]:
        response = self._session.get(SOL_TOKEN_LIST_URL)
        token_list = response.json()
        return {t['address']: t for t in token_list['content'] if t['chainId'] == 101}

    def _get_token_map_jup_ag(self) -> Dict[str, Dict]:
        response = self._session.get(JUP_AG_TOKEN_LIST_URL)

        csv_rows = response.text.split('\n')
        header = csv_rows[0].split(',')
        rows = [
            {header[i]: v for i, v in enumerate(row.split(','))} for row in csv_rows[1:]
        ]

        return {
            r['Mint']: {
                'address': r['Mint'],
                'chainId': 101,
                'name': r['Name'],
                'symbol': r['Symbol'],
                'verified': True,
                'decimals': r['Decimals'],
                'logoURI': r['LogoURI'],
                'tags': [],
                'extensions': {},
            }
            for r in rows
            if 'Mint' in r
        }

    def _get_token_map_sonar(self) -> Dict[str, Dict]:
        response = self._session.get(SONAR_TOKEN_LIST_URL)
        token_list = response.json()
        return {t['address']: t for t in token_list['tokens'] if t['chainId'] == 101}

    @property
    def ban_list(self) -> set[str]:
        if self._ban_list is None:
            response = self._session.get(JUP_AG_BAN_LIST_URL)
            ban_list = response.text.strip().split('\n')
            self._ban_list = set(i.split(',')[0] for i in ban_list[1:])
        return self._ban_list

    def fetch_balances(self, address: str) -> FetchResult:
        data = self._request(method='getBalance', params=[address])
        raw_token_balances = self._request(
            method='getTokenAccountsByOwner',
            params=[
                address,
                {'programId': self.token_program_id},
                {'encoding': 'jsonParsed'},
            ],
        )
        raw_token2022_balances = self._request(
            method='getTokenAccountsByOwner',
            params=[
                address,
                {'programId': self.token2022_program_id},
                {'encoding': 'jsonParsed'},
            ],
        )
        raw_staked_sol = self._fetch_staked_sol(address)
        raw_rent_reserve = self._fetch_stake_rent_reserve(raw_staked_sol)

        return FetchResult(
            data=data,
            extra=dict(
                raw_token_balances=raw_token_balances,
                raw_token2022_balances=raw_token2022_balances,
                raw_staked_sol=raw_staked_sol,
                raw_rent_reserve=raw_rent_reserve,
            ),
        )

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

    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        raw_token_balances = fetch_result.extra['raw_token_balances']
        raw_token2022_balances = fetch_result.extra['raw_token2022_balances']
        raw_staked_sol = fetch_result.extra['raw_staked_sol']
        raw_rent_reserve = fetch_result.extra['raw_rent_reserve']

        balances = []
        if sol_balance := self._get_sol_balance(fetch_result.data):
            balances.append(sol_balance)

        if staked_sol_balance := self._get_staked_sol_balance(raw_staked_sol):
            balances.append(staked_sol_balance)
            rent_reserve_balance = self._get_stake_rent_reserve(
                staked_sol_balance, raw_rent_reserve
            )
            balances.append(rent_reserve_balance)

        token_balances = list(self._yield_token_balances(raw_token_balances))
        token_balances.extend(self._yield_token_balances(raw_token2022_balances))

        if token_balances:
            merged_token_balances = self.merge_balances_with_same_coin(token_balances)
            balances.extend(merged_token_balances)

        return ParseResult(data=balances)

    @staticmethod
    def merge_balances_with_same_coin(
        token_balances: list[BalanceItem],
    ) -> list[BalanceItem]:
        return list(
            reduceby(
                key=lambda b: b.coin.address,
                binop=lambda v1, v2: v1 + v2,
                seq=token_balances,
            ).values()
        )

    def _get_sol_balance(
        self,
        response: dict,
    ) -> Optional[BalanceItem]:
        if int(response['result']['value']) == 0:
            return

        return BalanceItem.from_api(
            balance_raw=response['result']['value'],
            coin=self.coin,
            last_updated=None,
            raw=response,
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

    def _yield_token_balances(self, response: dict) -> Iterable[BalanceItem]:
        for raw_balance in response['result']['value']:
            balance = self._parse_token_balance(raw_balance)
            if balance is not None:
                yield balance

    def _parse_token_balance(self, raw: Dict) -> Optional[BalanceItem]:
        info = raw['account']['data']['parsed']['info']
        if int(info['tokenAmount']['amount']) == 0:
            return

        address = info['mint']

        # ignore banned tokens
        if address in self.ban_list:
            return

        # TODO unknown token is for 99% NFT, add loading NFT metadata using metaplex
        #  token account
        # TODO move fetching tokens_map to fetch
        if address not in self.tokens_map:
            if not self.update_token_from_metaplex(
                address, decimals=info['tokenAmount']['decimals']
            ):
                return

        return BalanceItem.from_api(
            balance_raw=info['tokenAmount']['amount'],
            coin=self.get_token_data(address),
            raw=raw,
        )

    def get_token_data(self, address: str) -> Coin:
        raw_token = self.tokens_map[address]
        extensions = raw_token.get('extensions', {})

        return Coin(
            symbol=raw_token['symbol'],
            name=raw_token['name'],
            decimals=raw_token['decimals'],
            blockchain=Blockchain.SOLANA if raw_token['chainId'] == 101 else None,
            address=address,
            standards=['SPL'],
            info=CoinInfo.from_api(
                tags=raw_token.get('tags'),
                logo_url=raw_token.get('logoURI'),
                # TODO sometimes coingeckoId is not mapped correctly
                # coingecko_id=extensions.get('coingeckoId'),
                website=extensions.get('website'),
            ),
        )

    def update_token_from_metaplex(self, address: str, decimals: int) -> bool:
        if not self.fetch_metaplex:
            return False

        pda = self.get_metadata_pda(address)
        content = self.fetch_metaplex_account(pda)
        token = self.parse_metaplex_account(content, decimals)
        if not token or not token.get('symbol'):
            return False

        self.tokens_map[address] = token
        return True

    def get_metadata_pda(self, mint_address: str) -> str:
        """
        Derives Metaplex metadata address from mint address

        :param mint_address: Token mint to get metadata for, e.g. `8ZperFA2cciv2rN2YC1QC3YjkuGcTQYiq9vc9aKmdoWM`
        :return: Token metadata account
        """
        return str(
            Pubkey.find_program_address(
                [
                    b"metadata",
                    bytes(self.METADATA_PROGRAM_ID),
                    bytes(Pubkey.from_string(mint_address)),
                ],
                self.METADATA_PROGRAM_ID,
            )[0]
        )

    def fetch_metaplex_account(self, metadata_pda: str) -> Optional[str]:
        """
        Fetch and validate metaplex account content
        :param metadata_pda: address of metadata account
        :return: base64 encoded account content
        """
        response = self._request(
            'getAccountInfo', [metadata_pda, {"encoding": "base64"}]
        )
        value = response['result']['value']
        if value:
            data = value['data'][0]
            if value['data'][1] != 'base64':
                return None

            if value['owner'] != 'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s':
                return None

            return data

        return None

    def parse_metaplex_account(self, content: str, decimals: int) -> Optional[dict]:
        if not content:
            return None

        raw = base64.b64decode(content)

        url = raw[119:255].decode('utf-8').rstrip('\x00')
        try:
            data = requests.get(url)
        except Exception as e:
            logger.exception(e)
            data = None

        if data:
            try:
                data.raise_for_status()
                parsed = data.json()
                return dict(
                    name=parsed.get('name'),
                    symbol=parsed.get('symbol'),
                    tags=parsed.get('tags'),
                    logoURI=parsed.get('image'),
                    decimals=decimals,
                    chainId=101,
                )
            except Exception as e:
                logger.exception(e)

        return dict(
            name=raw[69:101].decode('utf-8').rstrip('\x00'),
            symbol=raw[105:115].decode('utf-8').rstrip('\x00'),
            decimals=decimals,
            chainId=101,
        )

    def _request(self, method, params):
        body = json.dumps(
            {'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}
        )
        return self.post(body=body, headers={'Content-Type': 'application/json'})

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
