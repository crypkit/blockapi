import logging
from decimal import Decimal
from functools import lru_cache

import attr

from blockapi.v2.api.cosmos import CosmosApiBase
from blockapi.v2.base import ApiException, ApiOptions
from blockapi.v2.coins import COIN_TERRA
from blockapi.v2.models import BalanceItem, Blockchain, Coin

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

    def get_balance(
        self, address: str, merge_duplicates: bool = True
    ) -> list[BalanceItem]:
        balances = super().get_balance(address)
        if merge_duplicates:
            balances = self._merge_duplicate_balances(balances)
        return balances

    @staticmethod
    def _merge_duplicate_balances(
        balances: list[BalanceItem],
    ) -> list[BalanceItem]:
        """
        Merge balances that map to the same upstream coin (same coingecko_id
        + asset_type) into a single BalanceItem. Distinct IBC denoms that
        resolve to the same currency (e.g. SCRT via two channels) collapse
        into one entry. Items without a coingecko_id are left untouched to
        avoid collapsing unrelated unknown tokens.

        Merged items carry `raw = {'merged': [...originals], 'merged_count': N}`.
        """
        groups: dict[tuple, list[BalanceItem]] = {}
        order: list[tuple] = []

        for idx, b in enumerate(balances):
            coingecko_id = b.coin.info.coingecko_id if b.coin and b.coin.info else None
            if coingecko_id:
                key = (str(coingecko_id), b.asset_type)
            else:
                key = ('__unique__', idx)
            if key not in groups:
                groups[key] = []
                order.append(key)
            groups[key].append(b)

        merged: list[BalanceItem] = []
        for key in order:
            group = groups[key]
            if len(group) == 1:
                merged.append(group[0])
                continue
            head = group[0]
            merged.append(
                attr.evolve(
                    head,
                    balance=sum((b.balance for b in group), Decimal(0)),
                    balance_raw=sum((b.balance_raw for b in group), Decimal(0)),
                    raw={
                        'merged': [b.raw for b in group],
                        'merged_count': len(group),
                    },
                )
            )

        return merged

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
