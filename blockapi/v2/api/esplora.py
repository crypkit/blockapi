from blockapi.v2.base import ApiException, BalanceMixin, BlockchainApi
from blockapi.v2.coins import COIN_BTC
from blockapi.v2.models import (
    ApiOptions,
    AssetType,
    BalanceItem,
    Blockchain,
    FetchResult,
    ParseResult,
)


class EsploraApi(BlockchainApi, BalanceMixin):
    """Confirmed BTC address balances from an Esplora-compatible API.

    Defaults to Blockstream. Custom base URLs must include the API path
    (e.g. https://example.com/api/). Extended public keys are not supported.
    Docs: https://github.com/Blockstream/esplora/blob/master/API.md
    """

    coin = COIN_BTC
    api_options = ApiOptions(
        blockchain=Blockchain.BITCOIN,
        base_url='https://blockstream.info/api/',
        rate_limit=0.2,
    )
    supported_requests = {'get_balance': 'address/{address}'}
    request_timeout = (5, 15)

    def __init__(self, base_url=None, api_key=None, sleep_provider=None):
        super().__init__(api_key=api_key, sleep_provider=sleep_provider)
        self.base_url = (base_url or self.base_url).rstrip('/') + '/'

    def _get_response(self, request_method, headers, params, req_args):
        return self._session.get(
            self._build_request_url(request_method, **req_args),
            headers=headers,
            params=params,
            timeout=self.request_timeout,
        )

    def fetch_balances(self, address: str) -> FetchResult:
        if address.startswith(('xpub', 'ypub', 'zpub', 'tpub', 'upub', 'vpub')):
            return FetchResult(errors=['Esplora does not support extended public keys'])
        try:
            return self.get_data('get_balance', address=address)
        except ValueError:
            # The shared HTTP helper decodes JSON outside its exception handler.
            return FetchResult(errors=['Invalid JSON in Esplora response'])

    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        if fetch_result.errors:
            raise ApiException(fetch_result.errors[0])
        data = fetch_result.data
        stats = data.get('chain_stats') if isinstance(data, dict) else None
        if not isinstance(stats, dict):
            raise ApiException('Invalid Esplora response: missing chain_stats')
        funded = stats.get('funded_txo_sum')
        spent = stats.get('spent_txo_sum')
        if (
            type(funded) is not int
            or type(spent) is not int
            or funded < 0
            or spent < 0
            or spent > funded
        ):
            raise ApiException('Invalid Esplora response: invalid confirmed totals')

        # Exclude mempool deltas to preserve Haskoin's confirmed-only semantics.
        balance_raw = funded - spent
        if balance_raw == 0:
            return ParseResult()
        return ParseResult(
            data=[
                BalanceItem.from_api(
                    balance_raw=balance_raw,
                    coin=self.coin,
                    asset_type=AssetType.AVAILABLE,
                    raw=data,
                )
            ]
        )


class MempoolSpaceApi(EsploraApi):
    """Confirmed BTC address balances using mempool.space's Esplora API."""

    api_options = ApiOptions(
        blockchain=Blockchain.BITCOIN,
        base_url='https://mempool.space/api/',
        rate_limit=0.2,
    )
