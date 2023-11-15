from blockapi.v2.api.covalenth.base import CovalentApiBase
from blockapi.v2.base import ApiOptions
from blockapi.v2.coins import COIN_BTC
from blockapi.v2.models import Blockchain


class BitcoinCovalentApi(CovalentApiBase):
    CHAIN_ID = 'btc-mainnet'

    api_options = ApiOptions(
        blockchain=Blockchain.BITCOIN,
        base_url=CovalentApiBase.API_BASE_URL,
        rate_limit=0.25,
    )

    coin = COIN_BTC
