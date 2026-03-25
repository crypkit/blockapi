import logging
from functools import lru_cache

from blockapi.v2.api.cosmos import CosmosApiBase
from blockapi.v2.base import ApiException, ApiOptions
from blockapi.v2.coins import COIN_TERRA
from blockapi.v2.models import Blockchain, Coin

logger = logging.getLogger(__name__)


class TerraApi(CosmosApiBase):
    """
    Terra Classic (LUNC) via standard Cosmos LCD endpoints.
    Explorer: https://finder.terra.money
    """

    coin = COIN_TERRA
    TOKENS_MAP_BLOCKCHAIN_KEY = 'terra'
    api_options = ApiOptions(
        blockchain=Blockchain.TERRA,
        base_url='https://terra-classic-fcd.publicnode.com/',
        rate_limit=CosmosApiBase.API_BASE_RATE_LIMIT,
    )

    supported_requests = {
        **CosmosApiBase.supported_requests,
        'get_ibc_denom_trace': '/ibc/apps/transfer/v1/denom_traces/{hash}',
    }

    def create_default_coin(self, denom: str) -> Coin:
        if denom.startswith('ibc/'):
            return self._resolve_ibc_denom(denom)

        return super().create_default_coin(denom)

    @lru_cache(maxsize=64)
    def _resolve_ibc_denom(self, denom: str) -> Coin:
        hash_ = denom.split('/')[1]
        try:
            response = self.get('get_ibc_denom_trace', hash=hash_)
            base_denom = response['denom_trace']['base_denom']
            symbol = (
                base_denom.lstrip('ux').upper()
                if base_denom.startswith(('u', 'x'))
                else base_denom.upper()
            )
        except (ApiException, KeyError) as e:
            logger.warning(f'Failed to resolve IBC denom {denom}: {e}')
            return super().create_default_coin(denom)

        return Coin.from_api(
            symbol=symbol,
            name=symbol,
            decimals=self.coin.decimals,
            blockchain=self.api_options.blockchain,
            address=denom,
            standards=['ibc'],
        )
