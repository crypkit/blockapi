from typing import Iterable, List

from blockapi.v2.base import BlockchainApi, IBalance
from blockapi.v2.coins import COIN_SUI
from blockapi.v2.models import ApiOptions, BalanceItem, Blockchain, Coin


class SuiApi(BlockchainApi, IBalance):

    coin = COIN_SUI

    api_options = ApiOptions(
        blockchain=Blockchain.SUI,
        base_url="https://suiscan.xyz",
        rate_limit=0.25,  # 4 per second
    )

    supported_requests = {
        'get_balances': '/api/sui-backend/mainnet/api/accounts/{address}/objects',
    }

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
                balance_raw=response_coin.get('objectCount', 0),
                coin=coin,
                raw=response_coin,
            )

    def _post(self, request_method: str, address) -> dict:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
            'Origin': 'https://suiscan.xyz/',
        }

        json_request = {"objectTypes": ["coin"]}
        return self.post(
            request_method=request_method,
            headers=headers,
            json=json_request,
            address=address,
        )
