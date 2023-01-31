from abc import ABCMeta
from decimal import Decimal
from typing import Iterable, Optional

from blockapi.utils.num import to_decimal
from blockapi.v2.base import ApiOptions, BlockchainApi, IBalance
from blockapi.v2.coins import COIN_ATOM
from blockapi.v2.models import AssetType, BalanceItem, Blockchain, Coin


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

    _tokens_map: Optional[dict[str, dict]] = None

    @property
    def tokens_map(self) -> dict[str, dict]:
        return NotImplemented

    def get_balance(self, address: str) -> list[BalanceItem]:
        balances = []

        balances.extend(list(self._yield_available_balance(address)))
        if staked_balance := self._get_staked_balance(address):
            balances.append(staked_balance)
        if reward_balance := self._get_reward_balance(address):
            balances.append(reward_balance)

        return balances

    def _yield_available_balance(self, address: str) -> Iterable[BalanceItem]:
        response = self._get('get_balances', address=address)

        for b in response['balances']:
            if b['denom'] == self.coin.address:
                yield BalanceItem.from_api(
                    balance_raw=b['amount'], coin=self.coin, raw=b
                )
            else:
                if b['denom'] in self.tokens_map:
                    token = self._get_token_data(b['denom'])
                else:
                    token = Coin.from_api(
                        blockchain=Blockchain.COSMOS,
                        decimals=self.coin.decimals,
                        address=b['denom'],
                    )
                yield BalanceItem.from_api(balance_raw=b['amount'], coin=token, raw=b)

    def _get_token_data(self, denom: str) -> Coin:
        raw_token = self.tokens_map[denom]
        return Coin(
            symbol=raw_token['dp_denom'],
            name=raw_token['dp_denom'],
            decimals=raw_token['decimal'],
            blockchain=Blockchain.COSMOS,
            address=raw_token['base_denom'],
            standards=raw_token['type'],
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

    def _get_reward_balance(self, address: str) -> Optional[BalanceItem]:
        response = self._get('get_rewards', address=address)
        if not response.get('rewards'):
            return

        return BalanceItem.from_api(
            balance_raw=response['total'][0]['amount'],
            coin=self.coin,
            asset_type=AssetType.REWARDS,
            raw=response['total'],
        )

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
    api_options = ApiOptions(
        blockchain=Blockchain.COSMOS,
        base_url=CosmosApiBase.API_BASE_URL,
        rate_limit=CosmosApiBase.API_BASE_RATE_LIMIT,
    )

    @property
    def tokens_map(self) -> dict[str, dict]:
        if self._tokens_map is None:
            response = self._session.get('https://api.mintscan.io/v2/assets/cosmos')
            token_list = response.json()
            if 'assets' not in token_list:
                self._tokens_map = {}
            else:
                self._tokens_map = {a['denom']: a for a in token_list['assets']}

        return self._tokens_map
