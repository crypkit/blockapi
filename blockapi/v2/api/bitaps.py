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


class BitapsLitecoinApi(BlockchainApi, BalanceMixin):
    """
    Coin: Litecoin
    API docs: https://developer.bitaps.com/
    Explorer: https://ltc.bitaps.com
    """

    coin = COIN_LTC
    api_options = ApiOptions(
        blockchain=Blockchain.LITECOIN,
        base_url='https://api.bitaps.com/ltc/v1/',
        rate_limit=0.1,
    )

    supported_requests = {
        'get_balance': 'blockchain/address/state/{address}',
    }

    def fetch_balances(self, address: str) -> FetchResult:
        return self.get_data('get_balance', address=address)

    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result.data:
            return ParseResult()

        data = fetch_result.data.get('data', {})
        balance_raw = data.get('balance')

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
