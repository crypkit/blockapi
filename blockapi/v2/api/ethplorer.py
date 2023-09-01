from typing import Dict, Iterable, Optional

from eth_utils import to_checksum_address

from blockapi.v2.base import ApiOptions, BalanceMixin, BlockchainApi
from blockapi.v2.coins import COIN_ETH
from blockapi.v2.models import (
    BalanceItem,
    Blockchain,
    Coin,
    CoinInfo,
    FetchResult,
    ParseResult,
)


class EthplorerApi(BlockchainApi, BalanceMixin):
    """
    Ethereum
    API docs: https://github.com/EverexIO/Ethplorer/wiki/Ethplorer-API
    Explorer: https://ethplorer.io
    """

    coin = COIN_ETH
    api_options = ApiOptions(
        blockchain=Blockchain.ETHEREUM,
        base_url='https://api.ethplorer.io',
        rate_limit=0.2,  # 0.1 in case of api_key
    )

    supported_requests = {'get_info': '/getAddressInfo/{address}?apiKey={api_key}'}

    def __init__(self, api_key: str = 'freekey'):
        super().__init__(api_key)

    def fetch_balances(self, address: str) -> FetchResult:
        return self.get_data(
            'get_info',
            address=address,
            api_key=self.api_key,
        )

    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        response = fetch_result.data
        balances = []
        _eth = self._parse_eth_balance(response)
        if _eth is not None:
            balances.append(_eth)

        balances.extend(list(self._parse_token_balances(response)))

        return ParseResult(data=balances)

    def _parse_eth_balance(self, response: Dict) -> Optional[BalanceItem]:
        _eth_raw = response['ETH']
        if int(_eth_raw['rawBalance']) == 0:
            return

        return BalanceItem.from_api(
            balance_raw=_eth_raw['rawBalance'],
            coin=self.coin,
            last_updated=None,
            raw=_eth_raw,
        )

    def _parse_token_balances(self, response: Dict) -> Iterable[BalanceItem]:
        for _token_raw in response.get('tokens', []):
            if _token_raw.get('rawBalance') is None or _token_raw['rawBalance'] == 0:
                continue

            info = _token_raw['tokenInfo']
            coin = Coin.from_api(
                blockchain=self.api_options.blockchain,
                decimals=info.get('decimals', 0),
                symbol=info.get('symbol'),
                name=info.get('name'),
                address=to_checksum_address(info['address']),
                standards=None,  # parse from tags?
                info=CoinInfo.from_api(
                    tags=info.get('publicTags'),
                    total_supply=info.get('totalSupply'),
                    logo_url=(
                        self._format_logo_url(info.get('image'))
                        if info.get('image')
                        else None
                    ),
                    coingecko_id=info.get('coingecko'),
                    website=info.get('website'),
                ),
            )

            yield BalanceItem.from_api(
                balance_raw=_token_raw['rawBalance'],
                coin=coin,
                last_updated=info.get('lastUpdated'),
                raw=_token_raw,
            )

    @staticmethod
    def _format_logo_url(raw_url: str) -> str:
        return f'https://ethplorer.io{raw_url}'
