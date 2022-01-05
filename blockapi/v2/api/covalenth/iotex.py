from blockapi.v2.api.covalenth.base import CovalentApiBase
from blockapi.v2.base import ApiOptions
from blockapi.v2.coins import COIN_IOTX
from blockapi.v2.models import Blockchain


class IoTEXCovalentApi(CovalentApiBase):

    CHAIN_ID = 4689

    api_options = ApiOptions(
        blockchain=Blockchain.IOTEX,
        base_url=CovalentApiBase.API_BASE_URL,
        rate_limit=CovalentApiBase.API_BASE_RATE_LIMIT,
    )

    coin = COIN_IOTX
