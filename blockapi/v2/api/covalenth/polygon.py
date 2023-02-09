from blockapi.v2.api.covalenth.base import CovalentApiBase
from blockapi.v2.base import ApiOptions
from blockapi.v2.coins import COIN_MATIC
from blockapi.v2.models import Blockchain


class PolygonCovalentApi(CovalentApiBase):
    CHAIN_ID = 137

    api_options = ApiOptions(
        blockchain=Blockchain.POLYGON,
        base_url=CovalentApiBase.API_BASE_URL,
        rate_limit=CovalentApiBase.API_BASE_RATE_LIMIT,
    )

    coin = COIN_MATIC
