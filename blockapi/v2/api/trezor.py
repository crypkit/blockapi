from abc import ABC
from typing import List

from blockapi.utils.user_agent import get_random_user_agent
from blockapi.v2.base import BalanceMixin, BlockchainApi, ITransactions
from blockapi.v2.coins import COIN_BTC, COIN_LTC
from blockapi.v2.models import (
    ApiOptions,
    AssetType,
    BalanceItem,
    Blockchain,
    FetchResult,
    OperationDirection,
    OperationItem,
    OperationType,
    ParseResult,
    TransactionItem,
    TransactionStatus,
)


class TrezorApi(BlockchainApi, ITransactions, BalanceMixin, ABC):
    """
    Coins: Bitcoin, Litecoin
    API docs: https://github.com/trezor/blockbook/blob/master/docs/api.md
    Explorer:
    """

    supported_requests = {
        'get_balance': '/api/v2/address/{address}',
        'get_balance_xpub': '/api/v2/xpub/{address}',
        'get_txs': '/api/v2/utxo/{address}?confirmed={confirmed}',
        'get_tx': '/api/v2/tx/{tx_hash}',
    }

    def fetch_balances(self, address: str) -> FetchResult:
        request = 'get_balance_xpub' if len(address) == 111 else 'get_balance'
        return self.get_data(
            request,
            address=address,
            headers={'User-Agent': get_random_user_agent()},
        )

    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        if not fetch_result.data:
            return ParseResult()

        balances = [
            BalanceItem.from_api(
                balance_raw=fetch_result.data.get('balance'),
                coin=self.coin,
                asset_type=AssetType.AVAILABLE,
                raw=fetch_result.data,
            )
        ]

        return ParseResult(data=balances)

    def get_transactions(
        self,
        address: str,
        *,
        offset: int = 0,
        limit: int = 10,
        unconfirmed: bool = False
    ) -> List[TransactionItem]:
        response = self.get('get_txs', address=address, confirmed=not unconfirmed)

        return [self._parse_tx(address, tx) for tx in response]

    def _parse_tx(self, address: str, tx: dict) -> TransactionItem:
        txdata = self.get('get_tx', tx_hash=tx['txid'])

        if address in txdata['vin'][0]['addresses']:
            direction = OperationDirection.OUTGOING
        else:
            direction = OperationDirection.INCOMING

        return TransactionItem.from_api(
            fee_raw=txdata.get('fees'),
            coin=self.coin,
            date=txdata.get('blockTime'),
            hash=tx.get('txid'),
            status=(
                TransactionStatus.CONFIRMED
                if txdata['confirmations'] > 0
                else TransactionStatus.PENDING
            ),
            operations=[
                OperationItem.from_api(
                    amount_raw=txdata.get('value'),
                    coin=self.coin,
                    from_address=txdata['vin'][0]['addresses'],
                    to_address=txdata['vout'][0]['addresses'],
                    hash=tx.get('txid'),
                    type=OperationType.TRANSACTION,
                    direction=direction,
                    confirmed=txdata['confirmations'],
                    raw={},
                )
            ],
            raw=txdata,
        )


class TrezorBitcoin1Api(TrezorApi):
    coin = COIN_BTC
    api_options = ApiOptions(
        blockchain=Blockchain.BITCOIN,
        base_url='https://btc1.trezor.io',
        rate_limit=0,
    )


class TrezorBitcoin2Api(TrezorApi):
    coin = COIN_BTC
    api_options = ApiOptions(
        blockchain=Blockchain.BITCOIN,
        base_url='https://btc2.trezor.io',
        rate_limit=0,
    )


class TrezorLitecoinApi(TrezorApi):
    coin = COIN_LTC
    api_options = ApiOptions(
        blockchain=Blockchain.LITECOIN,
        base_url='https://ltc1.trezor.io',
        rate_limit=0,
    )
