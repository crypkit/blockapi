from typing import Literal, Optional

import base58

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

Derivation = Literal['legacy', 'compat', 'segwit']

# Version bytes for extended public keys (BIP32)
_XPUB_VERSION = bytes.fromhex('0488B21E')
_YPUB_VERSION = bytes.fromhex('049D7CB2')
_ZPUB_VERSION = bytes.fromhex('04B24746')

# Haskoin derive param: ypub -> compat (P2SH), zpub -> segwit (P2WPKH)
_DERIVE_TYPES = {
    'ypub': 'compat',
    'zpub': 'segwit',
}


def _to_xpub(key: str) -> str:
    """Convert ypub/zpub to xpub by replacing version bytes."""
    decoded = base58.b58decode_check(key)
    return base58.b58encode_check(_XPUB_VERSION + decoded[4:]).decode()


class HaskoinApi(BlockchainApi, BalanceMixin):
    """
    Coin: Bitcoin
    API docs: https://api.haskoin.com/
    Source: https://github.com/jprupp/haskoin-store

    Supports xpub, ypub (BIP49, P2SH-segwit), and zpub (BIP84, native segwit).
    ypub/zpub are converted to xpub and passed with the appropriate derive param.
    """

    coin = COIN_BTC
    api_options = ApiOptions(
        blockchain=Blockchain.BITCOIN,
        base_url='https://api.haskoin.com/btc/',
        rate_limit=0.2,
    )

    supported_requests = {
        'get_balance': 'address/{address}/balance',
        'get_balance_xpub': 'xpub/{address}',
    }

    def fetch_balances(
        self, address: str, *, derive: Optional[Derivation] = None
    ) -> FetchResult:
        """Follow Haskoin's SegWit hint once for a plain xpub without a derive override."""
        prefix = address[:4]
        if derive is not None and (
            prefix != 'xpub' or derive not in ('legacy', 'compat', 'segwit')
        ):
            return FetchResult(
                errors=['derive requires an xpub and legacy, compat, or segwit']
            )

        if prefix in _DERIVE_TYPES:
            derive = _DERIVE_TYPES[prefix]
            address = _to_xpub(address)
        elif prefix != 'xpub':
            return self.get_data('get_balance', address=address)

        if derive is None:
            result = self.get_data('get_balance_xpub', address=address)
            if result.status_code != 400 or not any(
                'ask with derive=segwit.' in error for error in result.errors or []
            ):
                return result
            if self.sleep_provider:
                self.sleep_provider.sleep(self.base_url, self.api_options.rate_limit)
            derive = 'segwit'

        return self.get_data(
            'get_balance_xpub', params={'derive': derive}, address=address
        )

    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result.data:
            return ParseResult()

        # xpub response: {"balance": {"confirmed": ...}, "indices": {...}}
        # address response: {"address": ..., "confirmed": ..., ...}
        if 'balance' in fetch_result.data:
            balance_raw = fetch_result.data['balance'].get('confirmed')
        else:
            balance_raw = fetch_result.data.get('confirmed')

        if not balance_raw:
            return ParseResult()

        balances = [
            BalanceItem.from_api(
                balance_raw=balance_raw,
                coin=self.coin,
                asset_type=AssetType.AVAILABLE,
                raw=fetch_result.data,
            )
        ]

        return ParseResult(data=balances)
