from blockapi.v2.base import BalanceMixin, BlockchainApi
from blockapi.v2.coins import COIN_LTC
from blockapi.v2.models import (
    ApiOptions,
    AssetType,
    BalanceItem,
    Blockchain,
    FetchResult,
    ParseResult,
)


class LitecoinSpaceApi(BlockchainApi, BalanceMixin):
    """
    Coin: Litecoin
    API docs: https://litecoinspace.org/docs/api/rest
    Explorer: https://litecoinspace.org
    """

    coin = COIN_LTC
    api_options = ApiOptions(
        blockchain=Blockchain.LITECOIN,
        base_url='https://litecoinspace.org',
        rate_limit=0.2,
    )

    supported_requests = {
        'get_balance': '/api/address/{address}',
    }

    def fetch_balances(self, address: str) -> FetchResult:
        return self.get_data('get_balance', address=address)

    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result.data:
            return ParseResult()

        chain_stats = fetch_result.data.get('chain_stats', {})
        funded = chain_stats.get('funded_txo_sum', 0)
        spent = chain_stats.get('spent_txo_sum', 0)
        balance_raw = funded - spent

        if not balance_raw:
            return ParseResult()

        return ParseResult(
            data=[
                BalanceItem.from_api(
                    balance_raw=balance_raw,
                    coin=self.coin,
                    asset_type=AssetType.AVAILABLE,
                    raw=fetch_result.data,
                )
            ]
        )
