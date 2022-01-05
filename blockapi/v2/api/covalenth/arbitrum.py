from blockapi.v2.api.covalenth.base import CovalentApiBase
from blockapi.v2.base import ApiOptions
from blockapi.v2.coins import COIN_ETH
from blockapi.v2.models import Blockchain


class ArbitrumCovalentApi(CovalentApiBase):

    CHAIN_ID = 42161

    api_options = ApiOptions(
        blockchain=Blockchain.ARBITRUM,
        base_url=CovalentApiBase.API_BASE_URL,
        rate_limit=CovalentApiBase.API_BASE_RATE_LIMIT,
    )

    coin = COIN_ETH
