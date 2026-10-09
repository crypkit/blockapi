from decimal import Decimal, InvalidOperation

from blockapi.v2.base import ApiException, BalanceMixin, BlockchainApi
from blockapi.v2.coins import COIN_LTC
from blockapi.v2.models import (
    ApiOptions,
    AssetType,
    BalanceItem,
    Blockchain,
    FetchResult,
    ParseResult,
)


class ChainSoLitecoinApi(BlockchainApi, BalanceMixin):
    """Litecoin confirmed balances: https://sochain.com/docs."""

    coin = COIN_LTC
    api_options = ApiOptions(
        blockchain=Blockchain.LITECOIN,
        base_url='https://sochain.com',
        rate_limit=1.0,
    )
    supported_requests = {
        'get_balance': '/api/v3/balance/LTC/{address}',
    }
    http_timeout = (3.0, 10.0)
    max_rate_limit_retries = 1

    def fetch_balances(self, address: str) -> FetchResult:
        return self.get_data('get_balance', address=address)

    def _get_response(self, request_method, headers, params, req_args):
        url = self._build_request_url(request_method, **req_args)
        return self._session.get(
            url, headers=headers, params=params, timeout=self.http_timeout
        )

    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        response = fetch_result.data
        if not isinstance(response, dict) or response.get('status') != 'success':
            raise ApiException('SoChain balance request was not successful')

        try:
            # SoChain returns LTC, whereas balance_raw uses litoshis.
            balance_raw = (
                Decimal(response['data']['confirmed']) * 10**self.coin.decimals
            )
        except (KeyError, TypeError, ValueError, InvalidOperation) as exc:
            raise ApiException('Invalid SoChain confirmed balance') from exc
        if (
            not balance_raw.is_finite()
            or balance_raw < 0
            or balance_raw != balance_raw.to_integral_value()
        ):
            raise ApiException('Invalid SoChain confirmed balance')
        if not balance_raw:
            return ParseResult()

        return ParseResult(
            data=[
                BalanceItem.from_api(
                    balance_raw=balance_raw,
                    coin=self.coin,
                    asset_type=AssetType.AVAILABLE,
                    raw=response,
                )
            ]
        )
