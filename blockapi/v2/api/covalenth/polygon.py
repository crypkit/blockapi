import logging

from blockapi.v2.api.covalenth.base import CovalentApiBase
from blockapi.v2.base import ApiOptions
from blockapi.v2.coins import coin_eth
from blockapi.v2.models import BalanceItem, Blockchain, Coin, CoinInfo

logger = logging.getLogger(__name__)


class MaticCovalentApi(CovalentApiBase):
    """
    API docs: https://www.covalenthq.com/docs/api/
    """

    CHAIN_ID = 137
    coin = coin_eth

    api_options = ApiOptions(
        blockchain=Blockchain.ETHEREUM,
        base_url=CovalentApiBase.API_BASE_URL,
        rate_limit=0.2,
    )

    def __init__(self, api_key: str):
        super().__init__(self.CHAIN_ID, api_key)
