from typing import Iterable, List

from blockapi.v2.base import BlockchainApi, IBalance
from blockapi.v2.coins import COIN_SUI
from blockapi.v2.models import ApiOptions, BalanceItem, Blockchain, Coin


class SuiApi(BlockchainApi, IBalance):

    coin = COIN_SUI

    api_options = ApiOptions(
        blockchain=Blockchain.SUI,
        base_url="https://api.blockberry.one",
        rate_limit=0.25,  # 4 per second
    )

    supported_requests = {
        'get_balances': '/sui/v1/accounts/{address}/objects',
    }

    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._headers = {'accept': 'application/json', 'x-api-key': api_key}

    def get_balance(self, address: str) -> List[BalanceItem]:
        balances = list(self._yield_available_balance(address))
        return balances

    def _yield_available_balance(self, address: str) -> Iterable[BalanceItem]:
        response = self._post('get_balances', address=address)

        for response_coin in response.get('coins', list()):
            coin = Coin.from_api(
                blockchain=Blockchain.SUI,
                decimals=response_coin.get('decimals'),
                symbol=response_coin.get('symbol'),
                name=response_coin.get('name'),
                address=response_coin.get('type'),
            )

            yield BalanceItem.from_api(
                balance_raw=response_coin.get('totalBalance', 0),
                coin=coin,
                raw=response_coin,
            )

    def _post(self, request_method: str, address) -> dict:

        json_request = {"objectTypes": ["coin"]}
        return self.post(
            request_method=request_method,
            headers=self._headers,
            json=json_request,
            address=address,
        )
