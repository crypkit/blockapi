from typing import Iterable, List, Optional

from blockapi.v2.base import BlockchainApi, IBalance
from blockapi.v2.coins import COIN_BOS
from blockapi.v2.models import (
    ApiOptions,
    AssetType,
    BalanceItem,
    Blockchain,
    OperationDirection,
    OperationItem,
    OperationType,
    TransactionItem,
    TransactionStatus,
)


class BlockchainosApi(BlockchainApi, IBalance):
    coin = COIN_BOS
    api_options = ApiOptions(
        blockchain=Blockchain.BOS,
        base_url='https://mainnet.blockchainos.org',
        rate_limit=0,
    )

    supported_requests = {
        'get_balance': '/api/v1/accounts/{address}',
        'get_txs': '/api/v1/accounts/{address}/transactions?limit={limit}&reverse=true',
        'get_ops': '/api/v1/transactions/{hash}/operations/{index}',
    }

    def get_balance(self, address: str) -> List[BalanceItem]:
        raw_balances = self.get('get_balance', address=address)
        return list(self._parse_balances(raw_balances))

    def get_transactions(
        self, address: str, *, limit: int = 10
    ) -> List[TransactionItem]:
        raw_transactions = self.get('get_txs', address=address, limit=limit)
        return list(self._parse_transactions(address, raw_transactions))

    def get_operations(
        self, address: str, hash_: str, count: int
    ) -> List[OperationItem]:
        ops = []
        for index in range(count):
            raw_operations = self.get('get_ops', hash=hash_, index=index)
            ops.extend(self._parse_operations(address, raw_operations))

        return ops

    def _parse_balances(self, raw_balances: dict) -> Iterable[BalanceItem]:
        yield BalanceItem.from_api(
            balance_raw=raw_balances.get('balance'),
            coin=self.coin,
            asset_type=AssetType.AVAILABLE,
            raw=raw_balances,
        )

    def _parse_transactions(
        self, address: str, raw_transactions: dict
    ) -> Iterable[TransactionItem]:
        records = self._get_records(raw_transactions)
        if not records:
            return

        for tx in records:
            hash_ = tx.get('hash')
            op_count = int(tx.get('operation_count'))
            yield TransactionItem.from_api(
                fee_raw=tx.get('fee'),
                coin=self.coin,
                date=tx.get('created'),
                hash=hash_,
                status=TransactionStatus.CONFIRMED,
                operations=self.get_operations(address, hash_, op_count),
                raw=raw_transactions,
            )

    def _parse_operations(self, address: str, raw_op: dict):
        body = raw_op.get('body')
        from_address = raw_op.get('source')
        yield OperationItem.from_api(
            amount_raw=body.get('amount'),
            coin=self.coin,
            from_address=from_address,
            to_address=raw_op.get('target'),
            hash=raw_op.get('tx_hash'),
            type=OperationType(raw_op.get('type')),
            direction=OperationDirection.OUTGOING
            if address == from_address
            else OperationDirection.INCOMING,
            raw=raw_op,
            confirmed=raw_op.get('confirmed'),
        )

    @staticmethod
    def _get_records(data: dict) -> Optional[dict]:
        embedded = data.get('_embedded')
        if not embedded:
            return None

        return embedded.get('records')
