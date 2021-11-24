from typing import List

from blockapi.v2.base import ApiException, ApiOptions, BlockchainApi
from blockapi.v2.coins import coin_terra
from blockapi.v2.models import AssetType, BalanceItem, Blockchain, Coin


class TerraMoneyApi(BlockchainApi):
    """
    Terra Money
    API docs: https://fcd.terra.dev/swagger
    Explorer: https://fcd.terra.dev/
    """

    coin = coin_terra
    api_options = ApiOptions(
        blockchain=Blockchain.TERRA,
        base_url='https://fcd.terra.dev/',
        rate_limit=0.5,
        start_offset=0,
        max_items_per_page=100,
        page_offset_step=1,
    )

    supported_requests = {
        'get_balance': '/v1/bank/{address}',
        'get_ibc_denom_trace': '/ibc/apps/transfer/v1/denom_traces/{hash}',
    }

    def get_balance(self) -> List[BalanceItem]:
        response = self.request('get_balance', address=self.address)

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

            # ?add other types: freedVesting, unbonding, ...

        for d in response['delegations']:
            if int(d['amount']) == 0:
                continue

            balances.append(
                BalanceItem.from_api(
                    balance_raw=d['amount'],
                    coin=self.coin,
                    asset_type=AssetType.STAKED,
                    raw=d,
                )
            )

        return balances

    @staticmethod
    def _get_terra_token_by_denom(denom: str) -> Coin:
        if denom == 'uluna':
            return coin_terra
        else:
            symbol = f'{denom[1:3].upper()}T'
            return Coin.from_api(
                symbol=symbol,
                name=symbol,
                decimals=6,
                blockchain=Blockchain.TERRA,
                address=denom,
                standards=['terra-native'],
            )

    def _get_ibc_token_by_denom(self, denom: str) -> Coin:
        hash_ = denom.split('/')[1]
        try:
            response = self.request('get_ibc_denom_trace', hash=hash_)
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
