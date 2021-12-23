import logging
from typing import Dict, Optional

from eth_utils import to_checksum_address

from blockapi.v2.api.covalenth.base import CovalentApiBase
from blockapi.v2.base import ApiOptions
from blockapi.v2.coins import coin_eth
from blockapi.v2.models import BalanceItem, Blockchain, Coin, CoinInfo

logger = logging.getLogger(__name__)


class EthCovalentApi(CovalentApiBase):
    """
    API docs: https://www.covalenthq.com/docs/api/
    """

    CHAIN_ID = 1
    coin = coin_eth

    api_options = ApiOptions(
        blockchain=Blockchain.ETHEREUM,
        base_url=CovalentApiBase.API_BASE_URL,
        rate_limit=0.2,
    )

    def __init__(self, address: str, api_key: str):
        super().__init__(self.CHAIN_ID, address, api_key)

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
                last_updated=None,  # TODO: similar item is "last_transferred_at" should I put it here?
                raw=raw_balance,
            )
