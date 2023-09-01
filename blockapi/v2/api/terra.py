import json
from functools import lru_cache
from typing import Dict, List, Optional, Sequence, Tuple

from cytoolz import concatv
from requests import Response

from blockapi.v2.base import (
    ApiException,
    ApiOptions,
    BalanceMixin,
    BlockchainApi,
    InvalidAddressException,
)
from blockapi.v2.coins import COIN_TERRA
from blockapi.v2.models import (
    AssetType,
    BalanceItem,
    Blockchain,
    Coin,
    CoinInfo,
    FetchResult,
    ParseResult,
)


class TerraApi(BalanceMixin):
    """
    Terra Money, implemented by multiple api providers.
    Explorer: https://finder.terra.money
    """

    coin = COIN_TERRA

    def __init__(self):
        self.mantle = TerraMantleApi()
        self.fcd = TerraFcdApi()

    def fetch_balances(self, address: str) -> FetchResult:
        status, balances, balance_errors = self.fcd.fetch_native_balances(address)
        _, staking_balances, staking_errors = self.fcd.fetch_staking_balances(address)
        cw20_balances = self.mantle.fetch_cw20_balances(address)

        return FetchResult(
            status_code=status,
            data=dict(
                balances=balances,
                raw_staking_balances=staking_balances,
                raw_cw20_balances=cw20_balances,
            ),
            errors=list(concatv(balance_errors, staking_errors)),
        )

    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        native_balances = self.fcd.parse_native_balances(
            fetch_result.data.get('balances')
        )
        staking_balances = self.fcd.parse_staking_balances(
            fetch_result.data.get('raw_staking_balances')
        )
        cw20_balances = self.mantle.parse_cw20_balances(
            fetch_result.data.get('raw_cw20_balances')
        )
        return ParseResult(
            data=list(concatv(native_balances, staking_balances, cw20_balances))
        )


class TerraFcdApi(BlockchainApi):
    """
    Terra Money FCD
    API docs: https://fcd.terra.dev/swagger
    """

    coin = COIN_TERRA
    api_options = ApiOptions(
        blockchain=Blockchain.TERRA,
        base_url='https://fcd.terra.dev/',
    )

    supported_requests = {
        'get_native_balances': '/v1/bank/{address}',
        'get_ibc_denom_trace': '/ibc/apps/transfer/v1/denom_traces/{hash}',
        'get_staking_data': '/v1/staking/{address}',
    }

    def fetch_native_balances(self, address: str) -> FetchResult:
        return self.get_data('get_native_balances', address=address)

    def parse_native_balances(self, response: dict) -> List[BalanceItem]:
        balances = []
        for b in response['balance']:
            if int(b['available']) == 0:
                continue

            coin = (
                self._get_terra_token_by_denom(b['denom'])
                if b['denom'].startswith('u')
                else self._get_ibc_token_by_denom(b['denom'])
            )

            balances.append(
                BalanceItem.from_api(balance_raw=b['available'], coin=coin, raw=b)
            )

        return balances

    def get_native_balances(self, address: str) -> List[BalanceItem]:
        _, response, _ = self.fetch_native_balances(address)
        return self.parse_native_balances(response)

    def fetch_staking_balances(self, address: str) -> FetchResult:
        return self.get_data('get_staking_data', address=address)

    def get_staking_balances(self, address: str) -> List[BalanceItem]:
        _, response, _ = self.fetch_staking_balances(address)
        return self.parse_staking_balances(response)

    def parse_staking_balances(self, response: dict) -> List[BalanceItem]:
        total_staked = 0
        balances = []

        # active stake
        if int(response['delegationTotal']) > 0:
            total_staked += int(response['delegationTotal'])
        # undelegated stake
        if response['undelegations']:
            total_staked += sum(int(u['amount']) for u in response['undelegations'])
        # total stake - sum of staked and undelegated
        # add redelegations?
        if total_staked:
            balances.append(
                BalanceItem.from_api(
                    balance_raw=total_staked,
                    coin=self.coin,
                    asset_type=AssetType.STAKED,
                    raw=response,
                )
            )

        # staking rewards
        for d in response['rewards']['denoms']:
            balances.append(
                BalanceItem.from_api(
                    balance_raw=d['amount'],
                    coin=self._get_terra_token_by_denom(d['denom']),
                    asset_type=AssetType.CLAIMABLE,
                    raw=d,
                )
            )

        return balances

    # It's possible to get cw20 balances, but it needs to be done one by one.
    # Use .terra_mantle.py for that
    # def get_cw20_balances(self):

    @staticmethod
    def _get_terra_token_by_denom(denom: str) -> Coin:
        if denom == 'uluna':
            return COIN_TERRA
        else:
            symbol = f'{denom[1:3].upper()}TC'
            return Coin.from_api(
                symbol=symbol,
                name=symbol,
                decimals=6,
                blockchain=Blockchain.TERRA,
                address=denom,
                standards=['terra-native'],
            )

    @lru_cache(maxsize=8)
    def _get_ibc_token_by_denom(self, denom: str) -> Coin:
        hash_ = denom.split('/')[1]
        try:
            response = self.get('get_ibc_denom_trace', hash=hash_)
        except ApiException:
            # add log
            symbol = None
        else:
            denom = response['denom_trace']['base_denom']
            symbol = denom[1:].upper()

        return Coin.from_api(
            symbol=symbol,
            name=symbol,
            decimals=6,
            blockchain=Blockchain.TERRA,
            address=hash_,
            standards=['ibc'],
        )


class TerraMantleApi(BlockchainApi):
    """
    Terra Money Subgraph API
    API docs: https://mantle.terra.dev
    """

    coin = COIN_TERRA
    api_options = ApiOptions(
        blockchain=Blockchain.TERRA,
        base_url='https://mantle.terra.dev',
    )

    # API uses post requests
    supported_requests = {}
    _post_requests = {
        'wasm_contract_address_store': """
            WasmContractsContractAddressStore(
                ContractAddress: "$CONTRACT_ADDRESS",
                QueryMsg: "$QUERY_MSG"
            ){
                Result
            }
        """
    }

    _tokens_map: Optional[Dict[str, Dict]] = None

    @property
    def tokens_map(self) -> Dict[str, Dict]:
        if self._tokens_map is None:
            response = self._session.get('https://assets.terra.money/cw20/tokens.json')
            token_list = response.json()
            self._tokens_map = token_list['classic']

        return self._tokens_map

    def fetch_cw20_balances(self, address) -> dict:
        return self._get_raw_balances(address)

    def get_cw20_balances(self, address: str):
        raw_balances = self._get_raw_balances(address)
        return self.parse_cw20_balances(raw_balances)

    def parse_cw20_balances(self, raw_balances):
        balances = []
        for contract, result_raw in raw_balances['data'].items():
            if not result_raw:
                # should be error in response, TODO add log
                continue

            data_raw = json.loads(result_raw['Result'])
            balance_raw = data_raw['balance']
            if int(balance_raw) == 0:
                continue

            balances.append(
                BalanceItem.from_api(
                    balance_raw=balance_raw,
                    coin=self._get_token_data(contract),
                    raw=result_raw,
                )
            )

        return balances

    def _get_token_data(self, address: str) -> Coin:
        raw_token = self.tokens_map[address]
        return Coin(
            symbol=raw_token['symbol'],
            name=raw_token['name'] if raw_token.get('name') else raw_token['symbol'],
            decimals=6,
            blockchain=Blockchain.TERRA,
            address=address,
            standards=['CW20'],
            protocol_id=raw_token.get('protocol'),
            info=CoinInfo.from_api(logo_url=raw_token.get('icon')),
        )

    def _get_raw_balances(self, address: str) -> Dict:
        cw20_contracts = list(self.tokens_map.keys())
        message = '{\\"balance\\": {\\"address\\": \\"$ADDR\\"}}'.replace(
            '$ADDR', address
        )

        key_queries = [
            self._create_key_query(
                key=contract,
                query=self._build_query(
                    method='wasm_contract_address_store',
                    params={'$CONTRACT_ADDRESS': contract, '$QUERY_MSG': message},
                ),
            )
            for contract in cw20_contracts
        ]
        query = self._concat_key_queries(key_queries)
        return self.post(json={'query': query})

    def _build_query(self, method: str, params: Optional[Dict[str, str]] = None) -> str:
        query = self._post_requests.get(method)
        if params:
            for k, v in params.items():
                query = query.replace(k, v)
        return query

    @staticmethod
    def _create_key_query(key: str, query: str) -> str:
        return f'{key}: {query}'

    @staticmethod
    def _concat_key_queries(key_queries: Sequence[str]) -> str:
        return '{' + ',\n'.join(key_queries) + '}'

    def _opt_raise_on_other_error(self, response: Response) -> None:
        json_response = response.json()
        if json_response.get('errors') is None:
            return

        # pick first message
        err = json_response['errors'][0]

        if 'addr_canonicalize' in err['message']:
            raise InvalidAddressException(f'Invalid address format.')
