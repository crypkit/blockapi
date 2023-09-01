from typing import Dict, List

from requests import Response

from blockapi.utils.user_agent import get_random_user_agent
from blockapi.v2.base import ApiException, ApiOptions, BalanceMixin, BlockchainApi
from blockapi.v2.coins import COIN_ETH
from blockapi.v2.models import BalanceItem, Blockchain, FetchResult, ParseResult


class OptimismEtherscanApi(BlockchainApi, BalanceMixin):
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

    def fetch_balances(self, address: str) -> FetchResult:
        return self.get_data(
            'get_balance',
            address=address,
            api_key=self.api_key,
            headers={'User-Agent': get_random_user_agent()},
        )

    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        data = fetch_result.data
        message = data.get('message')
        return ParseResult(
            data=[self._parse_eth_balance(data)],
            errors=message if message != 'OK' else None,
        )
