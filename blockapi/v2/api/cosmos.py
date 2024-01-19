import logging
from abc import ABCMeta
from collections import defaultdict
from decimal import Decimal
from typing import Iterable, Optional, Union

from requests import Session

from blockapi.utils.num import to_decimal
from blockapi.v2.base import ApiOptions, BlockchainApi, IBalance
from blockapi.v2.coins import COIN_ATOM, COIN_CELESTIA, COIN_DYDX, COIN_OSMOSIS
from blockapi.v2.models import AssetType, BalanceItem, Blockchain, Coin, CoinInfo

logger = logging.getLogger(__name__)


class CosmosTokenMapLoader:
    NATIVE_TOKEN_DATA_JSON = 'https://raw.githubusercontent.com/PulsarDefi/IBC-Token-Data-Cosmos/main/native_token_data.min.json'
    IBC_DATA_JSON = 'https://raw.githubusercontent.com/PulsarDefi/IBC-Token-Data-Cosmos/main/ibc_data.min.json'

    def __init__(self):
        self._session = Session()
        self._tokens_map = defaultdict(dict)

    @property
    def tokens_map(self) -> Union[defaultdict[str, dict], dict[str, dict]]:
        if not self._tokens_map:
            self.parse_native_tokens()
            self.parse_ibc_data()

        return self._tokens_map

    def parse_native_tokens(self):
        response = self._session.get(self.NATIVE_TOKEN_DATA_JSON)
        data = response.json()

        for key, value in data.items():
            native_denom, chain = key.split('__')
            self._tokens_map[chain][native_denom] = value

    def parse_ibc_data(self):
        response = self._session.get(self.IBC_DATA_JSON)
        data = response.json()

        for key, value in data.items():
            ibc_denom, chain = key.split('__')

            # Origin is link to already existing native token.
            native_token_chain = (
                value["origin"]["chain"][
                    0
                ]  # Just the first, BalanceItem has only one coin
                if isinstance(value["origin"]["chain"], list)
                else value["origin"]["chain"]
            )

            native_token_denom = value["origin"]["denom"]

            if native_token_denom not in self._tokens_map[native_token_chain]:
                logger.warning(
                    f"Skipping IBC {ibc_denom}, no native token: {native_token_denom}, chain: {native_token_chain}."
                )
                continue

            native_token_value = self._tokens_map[native_token_chain][
                native_token_denom
            ]

            self._tokens_map[chain][ibc_denom] = native_token_value


class CosmosApiBase(BlockchainApi, IBalance, metaclass=ABCMeta):
    """
    Cosmos RPC
    API docs: https://cosmos.network/rpc/
    Explorer: https://www.mintscan.io
    """

    coin = COIN_ATOM

    API_BASE_URL = 'https://lcd-cosmos.cosmostation.io/'
    API_BASE_RATE_LIMIT = 0.2

    supported_requests = {
        'get_balances': '/cosmos/bank/v1beta1/balances/{address}',
        'get_staked_balance': (
            '/cosmos/staking/v1beta1/delegations/{address}?pagination.limit=1000'
        ),
        'get_unbonding_balance': (
            '/cosmos/staking/v1beta1/delegators/{address}/unbonding_delegations'
        ),
        'get_rewards': 'cosmos/distribution/v1beta1/delegators/{address}/rewards',
        # TODO support commissions, valid only for validators?
        'get_commission': (
            'cosmos/distribution/v1beta1/validators/{validator_address}/commission'
        ),
    }

    TOKENS_MAP_BLOCKCHAIN_KEY = None

    def __init__(
        self,
        tokens_map: defaultdict[str, dict] = None,
        enable_token_mapping=True,
    ):
        super().__init__()
        self._tokens_map = tokens_map
        self.enable_token_mapping = enable_token_mapping

    @property
    def blockchain_tokens_map(self) -> dict[str, dict]:
        if not self._tokens_map:
            self._tokens_map = CosmosTokenMapLoader().tokens_map

        return self._tokens_map[self.TOKENS_MAP_BLOCKCHAIN_KEY]

    def get_balance(self, address: str) -> list[BalanceItem]:
        balances = []
        balances.extend(list(self._yield_available_balance(address)))
        if staked_balance := self._get_staked_balance(address):
            balances.append(staked_balance)
        if reward_balance := self._get_reward_balance(address):
            balances.extend(reward_balance)

        return balances

    def _yield_available_balance(self, address: str) -> Iterable[BalanceItem]:
        response = self._get('get_balances', address=address)

        for b in response['balances']:
            if b['denom'] == self.coin.address:
                yield BalanceItem.from_api(
                    balance_raw=b['amount'], coin=self.coin, raw=b
                )
            else:
                token = self.map_or_create_default(b['denom'])
                yield BalanceItem.from_api(balance_raw=b['amount'], coin=token, raw=b)

    def map_or_create_default(self, denom: str):
        token = self.map_to_native_token_if_enabled(denom)

        if not token:
            return self.create_default_coin(denom)

        return token

    def create_default_coin(self, denom: str):
        return Coin.from_api(
            blockchain=self.api_options.blockchain,
            decimals=self.coin.decimals,
            address=denom,
        )

    def map_to_native_token_if_enabled(self, denom: str):
        if not self.enable_token_mapping:
            return None

        if denom not in self.blockchain_tokens_map:
            return None

        return self._get_token_data(denom)

    def _get_token_data(self, denom: str) -> Coin:
        raw_token = self.blockchain_tokens_map[denom]
        return Coin(
            symbol=raw_token['symbol'],
            name=raw_token['name'],
            decimals=raw_token['decimals'],
            blockchain=self.api_options.blockchain,
            address=denom,  # We want original IBC address.
            standards=[],
            info=CoinInfo(coingecko_id=raw_token['coingecko_id']),
        )

    def _get_staked_balance(self, address: str) -> Optional[BalanceItem]:
        staked_response = self._get('get_staked_balance', address=address)
        staked_balance = sum(
            to_decimal(d['balance']['amount'])
            for d in staked_response['delegation_responses']
        )

        unbonding_response = self._get('get_unbonding_balance', address=address)
        unbonding_balance = sum(
            to_decimal(unbonding_entry['balance'])
            for unbonding in unbonding_response['unbonding_responses']
            for unbonding_entry in unbonding['entries']
        )

        # unbonding balance is still staked
        staked_balance += unbonding_balance
        if not staked_balance:
            return

        return BalanceItem.from_api(
            balance_raw=str(staked_balance),
            coin=self.coin,
            asset_type=AssetType.STAKED,
            raw={
                'delegated': staked_response['delegation_responses'],
                'unbonding': unbonding_response['unbonding_responses'],
            },
        )

    def _get_reward_balance(
        self, address: str, chain: str = 'cosmoshub'
    ) -> list[BalanceItem]:
        response = self._get('get_rewards', address=address)
        if not response.get('rewards'):
            return []

        rewards = []
        for reward in response['total']:
            token = self.map_or_create_default(reward['denom'])

            balance_reward = BalanceItem.from_api(
                balance_raw=reward['amount'],
                coin=token,
                asset_type=AssetType.REWARDS,
                raw=reward,
            )
            rewards.append(balance_reward)

        return rewards

    def _get_commission(self, validator_address: str) -> Decimal:
        response = self._get('get_commission', validator_address=validator_address)
        return to_decimal(response['commission']['commission'][0]['amount'])

    def _get(self, request_method: str, **req_args) -> dict:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/50.0.2661.102 Safari/537.36',
            'Referer': 'https://www.mintscan.io/',
        }
        return self.get(request_method, headers, **req_args)


class CosmosApi(CosmosApiBase):
    coin = COIN_ATOM
    TOKENS_MAP_BLOCKCHAIN_KEY = "cosmoshub"
    api_options = ApiOptions(
        blockchain=Blockchain.COSMOS,
        base_url=CosmosApiBase.API_BASE_URL,
        rate_limit=CosmosApiBase.API_BASE_RATE_LIMIT,
    )


class CosmosOsmosisApi(CosmosApiBase):
    coin = COIN_OSMOSIS
    TOKENS_MAP_BLOCKCHAIN_KEY = "osmosis"
    api_options = ApiOptions(
        blockchain=Blockchain.OSMOSIS,
        base_url='https://lcd-osmosis.cosmostation.io/',
        rate_limit=CosmosApiBase.API_BASE_RATE_LIMIT,
    )


class CosmosDydxApi(CosmosApiBase):
    coin = COIN_DYDX
    TOKENS_MAP_BLOCKCHAIN_KEY = "dydx"
    api_options = ApiOptions(
        blockchain=Blockchain.DYDX,
        base_url='https://lcd-dydx.cosmostation.io/',
        rate_limit=CosmosApiBase.API_BASE_RATE_LIMIT,
    )


class CosmosCelestiaApi(CosmosApiBase):
    coin = COIN_CELESTIA
    TOKENS_MAP_BLOCKCHAIN_KEY = "celestia"
    api_options = ApiOptions(
        blockchain=Blockchain.CELESTIA,
        base_url='https://lcd-celestia.cosmostation.io/',
        rate_limit=CosmosApiBase.API_BASE_RATE_LIMIT,
    )
