import json
from abc import ABC
from decimal import Decimal
from typing import Iterable, List, Optional

from requests import Response

from blockapi.utils.num import decimals_to_raw, safe_opt_decimal, to_decimal
from blockapi.v2.base import (
    ApiException,
    ApiOptions,
    BalanceMixin,
    BlockchainApi,
    InvalidAddressException,
)
from blockapi.v2.coins import COIN_DOT, COIN_KSM
from blockapi.v2.models import (
    AssetType,
    BalanceItem,
    Blockchain,
    FetchResult,
    ParseResult,
)


class SubscanApi(BlockchainApi, BalanceMixin, ABC):
    """
    API docs: https://docs.api.subscan.io/
    Explorer: https://www.subscan.io
    """

    coin = None
    api_options = None

    supported_requests = {
        'get_balance': '/api/v2/scan/search',
        'get_rewards': '/api/v2/scan/account/reward_slash',
    }

    def fetch_balances(self, address: str) -> FetchResult:
        body = json.dumps({'key': address})
        response = self._post('get_balance', body=body)
        return FetchResult(data=response)

    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        balances = list(self._yield_native_balances(fetch_result.data))

        # add staking rewards (and slashes) too? it's a lot of requests
        # per single address
        # if staking_reward := self._get_staking_reward(address):
        #     balances.append(staking_reward)

        return ParseResult(data=balances)

    def _yield_native_balances(self, response: dict) -> Iterable[BalanceItem]:
        data = response['data']['account']
        b_total = decimals_to_raw(data['balance'], self.coin.decimals)
        if b_total == 0:
            return []

        b_total_locked = decimals_to_raw(data['balance_lock'], self.coin.decimals)

        b_staked = Decimal(0)
        if data['staking_info']:
            b_staked = b_total_locked

        # ignore data['unbonding'] - it's still staked

        b_reserved = safe_opt_decimal(data['reserved'])
        b_vesting = (
            to_decimal(data['vesting']['total_locked'])
            if data['vesting']
            else Decimal(0)
        )

        # do we want to include these?
        # b_democracy = safe_opt_decimal(data['democracy_lock'])
        # b_election = safe_opt_decimal(data['election_lock'])

        b_available = b_total - b_total_locked - b_reserved
        b_locked = b_reserved

        if b_available:
            yield BalanceItem.from_api(
                balance_raw=int(b_available),
                coin=self.coin,
                asset_type=AssetType.AVAILABLE,
                raw=data,
            )

        if b_staked:
            yield BalanceItem.from_api(
                balance_raw=int(b_staked),
                coin=self.coin,
                asset_type=AssetType.STAKED,
                raw=data,
            )

        if b_vesting:
            yield BalanceItem.from_api(
                balance_raw=int(b_vesting),
                coin=self.coin,
                asset_type=AssetType.VESTING,
                raw=data['vesting'],
            )

        if b_locked:
            yield BalanceItem.from_api(
                balance_raw=int(b_locked),
                coin=self.coin,
                asset_type=AssetType.LOCKED,
                raw=data,
            )

    def _get_staking_reward(self, address: str) -> Optional[BalanceItem]:
        reward = sum(self._yield_staking_rewards(address))
        if not reward:
            return

        return BalanceItem.from_api(
            balance_raw=int(reward),
            coin=self.coin,
            asset_type=AssetType.REWARDS,
            raw={},
        )

    def _yield_staking_rewards(self, address: str) -> Iterable[Decimal]:
        body = {
            'address': address,
            'row': self.api_options.max_items_per_page,
            'page': 0,
        }
        continuous_count = 0

        while True:
            response = self._post('get_rewards', body=json.dumps(body))
            total_count = response['data']['count']
            continuous_count += len(response['data']['list'])

            for i in response['data']['list']:
                yield (
                    to_decimal(i['amount'])
                    if i['event_id'] == 'Rewarded'
                    else to_decimal(i['amount']) * -1
                )

            if continuous_count >= total_count:
                return

            body['page'] += self.api_options.page_offset_step

    def _post(self, request_method: str, body):
        headers = {'Content-Type': 'application/json'}
        return self.post(request_method, body=body, headers=headers)

    def _opt_raise_on_other_error(self, response: Response) -> None:
        json_response = response.json()
        code = json_response.get('code')

        if code == 10004:
            raise InvalidAddressException('Invalid address format.')
        elif code:
            raise ApiException(json_response['message'])

    @staticmethod
    def _get_api_options(blockchain: Blockchain, base_url: str) -> ApiOptions:
        return ApiOptions(
            blockchain=blockchain,
            base_url=base_url,
            start_offset=0,
            max_items_per_page=100,
            page_offset_step=1,
        )


class PolkadotSubscanApi(SubscanApi):
    coin = COIN_DOT
    api_options = SubscanApi._get_api_options(
        blockchain=Blockchain.POLKADOT, base_url='https://polkadot.api.subscan.io'
    )


class KusamaSubscanApi(SubscanApi):
    coin = COIN_KSM
    api_options = SubscanApi._get_api_options(
        blockchain=Blockchain.KUSAMA, base_url='https://kusama.api.subscan.io'
    )
