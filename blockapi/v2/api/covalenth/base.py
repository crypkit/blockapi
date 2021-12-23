from typing import Dict, Iterable, List, Optional

from blockapi.v2.base import ApiOptions, BlockchainApi
from blockapi.v2.models import BalanceItem


class CovalentApiBase(BlockchainApi):
    """
    API docs: https://www.covalenthq.com/docs/api/
    """

    API_BASE_URL = 'https://api.covalenthq.com/v1'

    coin = None  # TODO will be set in childs
    api_options = None  # TODO will be set in childs

    supported_requests = {
        'get_balance': '/v1/{chain_id}/address/{address}/balances_v2/'
    }

    def __init__(self, chain_id: int, address: str, api_key: str):
        super().__init__(address, api_key)
        self.chain_id = chain_id

        # Set http basic auth for requests.
        self._session.auth = (api_key, "")

    def get_balance(self) -> Optional[BalanceItem]:
        response = self.get('get_balance', chain_id=self.chain_id, address=self.address)

        return self._parse_items(response)

    def _parse_items(self, response: Dict) -> Optional[BalanceItem]:
        raise NotImplemented()
