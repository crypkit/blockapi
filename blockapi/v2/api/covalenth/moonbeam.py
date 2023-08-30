from blockapi.v2.api.covalenth.base import CovalentApiBase
from blockapi.v2.base import ApiOptions
from blockapi.v2.coins import COIN_MOVR
from blockapi.v2.models import Blockchain


class MoonBeamCovalentApi(CovalentApiBase):
    CHAIN_ID = 1285

    api_options = ApiOptions(
        blockchain=Blockchain.MOONRIVER,
        base_url=CovalentApiBase.API_BASE_URL,
        rate_limit=CovalentApiBase.API_BASE_RATE_LIMIT,
    )

    coin = COIN_MOVR
