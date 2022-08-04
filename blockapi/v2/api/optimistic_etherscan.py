from typing import Dict, List

from requests import Response

from blockapi.v2.base import ApiException, ApiOptions, BlockchainApi, IBalance
from blockapi.v2.coins import COIN_ETH
from blockapi.v2.models import BalanceItem, Blockchain


class OptimismEtherscanApi(BlockchainApi, IBalance):
    """
    Optimism
    Explorer: https://optimistic.etherscan.io
    """

    coin = COIN_ETH
    api_options = ApiOptions(
        blockchain=Blockchain.OPTIMISM,
        base_url='https://api-optimistic.etherscan.io/api',
        rate_limit=0.2,  # 0.1 in case of api_key
    )

    supported_requests = {
        'get_balance': '?module=account&action=balance&address={address}&tag=latest&apikey={api_key}'
    }

    def __init__(self, api_key: str = ''):
        super().__init__(api_key)

    def _parse_eth_balance(self, response: Dict) -> BalanceItem:
        return BalanceItem.from_api(
            balance_raw=response.get('result', 0),
            coin=self.coin,
            raw=response,
        )

    def get_balance(self, address: str) -> List[BalanceItem]:
        # TODO: currently returns only ETH balance (not all ERC20 tokens)
        response = self.get(
            'get_balance',
            address=address,
            api_key=self.api_key,
            # API requires User-Agent.
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, '
                'like Gecko) Chrome/50.0.2661.102 Safari/537.36'
            },
        )

        return [self._parse_eth_balance(response)]

    def _opt_raise_on_other_error(self, response: Response) -> None:
        json_response = response.json()
        if json_response["message"] == "OK":
            return

        raise ApiException(json_response['result'])
