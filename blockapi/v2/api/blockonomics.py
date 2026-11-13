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


class BlockonomicsApi(BlockchainApi, BalanceMixin):
    """BTC balances for addresses and xpub/ypub/zpub extended public keys.

    Requires a Blockonomics API key. Only provider-confirmed balances are
    included: Blockonomics classifies fewer than two confirmations as
    unconfirmed. Extended-key discovery follows the provider's gap policy.
    Docs: https://developers.blockonomics.co/docs/search/getbalance
    """

    coin = COIN_BTC
    api_options = ApiOptions(
        blockchain=Blockchain.BITCOIN,
        base_url='https://www.blockonomics.co/api/',
        rate_limit=1,
    )
    supported_requests = {'get_balance': 'balance'}
    request_timeout = (5, 30)

    def _get_response(self, request_method, headers, params, req_args):
        return self._session.get(
            self._build_request_url(request_method, **req_args),
            headers=headers,
            params=params,
            timeout=self.request_timeout,
        )

    def fetch_balances(self, address: str) -> FetchResult:
        if not self.api_key:
            return FetchResult(errors=['Blockonomics API key is required'])
        # One wallet per request; whitespace is the provider's batch separator.
        if not address or any(char.isspace() for char in address):
            return FetchResult(errors=['Expected one Bitcoin address or extended key'])
        try:
            return self.get_data(
                'get_balance',
                headers={'Authorization': f'Bearer {self.api_key}'},
                params={'addr': address},
            )
        except ValueError:
            return FetchResult(errors=['Invalid JSON in Blockonomics response'])

    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        if fetch_result.errors:
            raise ApiException(fetch_result.errors[0])
        data = fetch_result.data
        rows = data.get('response') if isinstance(data, dict) else None
        if not isinstance(rows, list) or not rows:
            raise ApiException('Invalid Blockonomics response: missing balance rows')
        addresses = set()
        balance_raw = 0
        for row in rows:
            if not isinstance(row, dict):
                raise ApiException('Invalid Blockonomics balance row')
            address = row.get('addr')
            confirmed = row.get('confirmed')
            if (
                not isinstance(address, str)
                or not address
                or address in addresses
                or type(confirmed) is not int
                or confirmed < 0
            ):
                raise ApiException('Invalid Blockonomics balance row')
            addresses.add(address)
            balance_raw += confirmed
        if not balance_raw:
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
