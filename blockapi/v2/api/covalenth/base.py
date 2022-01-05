import logging
from abc import ABCMeta, abstractmethod
from typing import Dict, Optional

from eth_utils import to_checksum_address

from blockapi.v2.base import BlockchainApi, IBalance
from blockapi.v2.models import BalanceItem, Coin, CoinInfo

logger = logging.getLogger(__name__)


class CovalentApiBase(BlockchainApi, IBalance, metaclass=ABCMeta):
    """
    API docs: https://www.covalenthq.com/docs/api/
    """

    API_BASE_URL = 'https://api.covalenthq.com/v1'
    API_BASE_RATE_LIMIT = 0.2

    @property
    @abstractmethod
    def api_options(self):
        pass

    @property
    @abstractmethod
    def CHAIN_ID(self):
        pass

    supported_requests = {
        'get_balance': '/v1/{chain_id}/address/{address}/balances_v2/'
    }

    def __init__(self, api_key: str):
        super().__init__(api_key)

        # Set http basic auth for requests.
        self._session.auth = (api_key, "")

    def get_balance(self, address: str) -> Optional[BalanceItem]:
        response = self.get('get_balance', chain_id=self.CHAIN_ID, address=address)

        return self._parse_items(response)

    def _parse_items(self, response: Dict) -> Optional[BalanceItem]:
        try:
            raw_balances = response['data']['items']
        except KeyError as e:
            logger.exception(e)
            return []

        for raw_balance in raw_balances:
            if raw_balance.get('balance') is None or raw_balance['balance'] == 0:
                logger.debug(
                    "Skipping coin: '%s' - balance is zero.",
                    raw_balance.get("contract_name"),
                )
                continue

            coin = Coin.from_api(
                symbol=raw_balance.get('contract_ticker_symbol'),
                name=raw_balance.get('contract_name'),
                decimals=raw_balance.get('contract_decimals', 0),
                blockchain=self.api_options.blockchain,
                address=to_checksum_address(raw_balance.get('contract_address')),
                standards=raw_balance.get("supports_erc", []),
                info=CoinInfo(logo_url=raw_balance.get("logo_url")),
            )

            yield BalanceItem.from_api(
                balance_raw=raw_balance.get('balance'),
                coin=coin,
                last_updated=None,
                # TODO: similar item is "last_transferred_at" should I put it here?
                raw=raw_balance,
            )
