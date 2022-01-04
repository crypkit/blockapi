from blockapi.v2.api.covalenth.base import CovalentApiBase
from blockapi.v2.base import ApiOptions
from blockapi.v2.models import Blockchain


class AstarCovalentApi(CovalentApiBase):

    CHAIN_ID = 336

    api_options = ApiOptions(
        blockchain=Blockchain.ASTAR,
        base_url=CovalentApiBase.API_BASE_URL,
        rate_limit=CovalentApiBase.API_BASE_RATE_LIMIT,
    )

    def __init__(self, api_key: str):
        super().__init__(self.CHAIN_ID, api_key)
