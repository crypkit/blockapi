from blockapi.v2.base import BalanceMixin, BlockchainApi
from blockapi.v2.coins import COIN_BTC
from blockapi.v2.models import (
    ApiOptions,
    AssetType,
    BalanceItem,
    Blockchain,
    FetchResult,
    ParseResult,
)


class BlockchainInfoApi(BlockchainApi, BalanceMixin):
    """
    Coin: Bitcoin
    API docs: https://www.blockchain.com/explorer/api/blockchain_api
    Explorer: https://www.blockchain.com/explorer
    """

    coin = COIN_BTC
    api_options = ApiOptions(
        blockchain=Blockchain.BITCOIN,
        base_url='https://blockchain.info',
        rate_limit=0.2,
    )

    supported_requests = {
        'get_balance': '/multiaddr',
    }

    def fetch_balances(self, address: str) -> FetchResult:
        return self.get_data(
            'get_balance',
            params={'active': address, 'n': 0},
        )

    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result.data:
            return ParseResult()

        wallet = fetch_result.data.get('wallet', {})
        if not wallet:
            return ParseResult()

        balances = [
            BalanceItem.from_api(
                balance_raw=wallet.get('final_balance'),
                coin=self.coin,
                asset_type=AssetType.AVAILABLE,
                raw=fetch_result.data,
            )
        ]

        return ParseResult(data=balances)
