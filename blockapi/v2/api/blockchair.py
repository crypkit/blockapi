from abc import ABC, abstractmethod
from typing import Iterable, List

from blockapi.utils.num import to_decimal
from blockapi.v2.base import BlockchainApi, IBalance
from blockapi.v2.coins import COIN_BTC
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


class BlockchairApi(BlockchainApi, IBalance, ABC):
    BASE_URL = 'https://api.blockchair.com'

    @property
    @abstractmethod
    def blockchain(self):
        pass

    @property
    @abstractmethod
    def coin(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    supported_requests = {
        'get_dashboard': '/{name}/dashboards/{address_type}/{address}?limit={limit},0&offset={offset},0',
        'get_txs': '/{name}/dashboards/transactions/{hash_or_hashes}',
    }

    def __init__(self):
        super().__init__()

        self.api_options = ApiOptions(
            blockchain=self.blockchain, base_url=self.BASE_URL, rate_limit=0
        )

    def get_balance(self, address: str) -> List[BalanceItem]:
        dashboard = self._get_dashboard(address)
        return list(self._parse_balances(dashboard))

    def get_transactions(
        self, address: str, *, offset: int = 0, limit: int = 10
    ) -> List[TransactionItem]:
        dashboard = self._get_dashboard(address, offset, limit)
        hashes = dashboard.get('transactions')
        if not hashes:
            return []

        transactions = self.get(
            'get_txs', name=self.name, hash_or_hashes=','.join(hashes)
        )

        data = transactions.get('data')
        if not data:
            return []

        return list(self._parse_transactions(address, data))

    def _get_dashboard(self, address, offset: int = 0, limit: int = 10):
        address_type = self._get_address_type(address)
        raw_dashboard = self.get(
            'get_dashboard',
            address=address,
            symbol=self.coin.symbol,
            address_type=address_type,
            name=self.name,
            offset=offset,
            limit=limit,
        )

        return self._parse_dashboard(raw_dashboard, address_type)

    @staticmethod
    def _get_address_type(address):
        is_xpub = any(address.startswith(p) for p in ['xpub', 'ypub', 'zpub'])

        return 'xpub' if is_xpub else 'address'

    @staticmethod
    def _parse_dashboard(dashboard: dict, address_type: str):
        data = dashboard.get('data')
        if not data:
            return

        item = list(data.values())[0]
        if address_type == 'address':
            adr = item.get('address')
            if not adr.get('type'):
                return

        return item

    def _parse_balances(self, dashboard: dict) -> Iterable[BalanceItem]:
        addr = dashboard.get('address')
        balance = addr.get('balance')

        yield BalanceItem.from_api(
            balance_raw=balance,
            coin=self.coin,
            asset_type=AssetType.AVAILABLE,
            raw=dashboard,
        )

    def _parse_transactions(
        self, address: str, data: dict
    ) -> Iterable[TransactionItem]:
        for tx in data.values():
            parsed = self._parse_transaction(address, tx)
            if parsed:
                yield parsed

    def _parse_transaction(self, address: str, tx: dict) -> TransactionItem:
        incoming = next(
            (i for i in tx.get('inputs') if address == i['recipient']), None
        )
        outgoing = next(
            (o for o in tx.get('outputs') if address == o['recipient']), None
        )

        tx_data = tx.get('transaction')

        if incoming:
            return TransactionItem.from_api(
                fee_raw=tx_data.get('fee'),
                coin=self.coin,
                date=tx.get('time'),
                hash=incoming.get('hash'),
                status=TransactionStatus.CONFIRMED,
                operations=[
                    OperationItem.from_api(
                        amount_raw=incoming.get('value'),
                        coin=self.coin,
                        to_address=address,
                        from_address=(
                            tx['inputs'][0]['recipient']
                            if tx_data['input_count'] == 1
                            else 'multiple'
                        ),
                        hash=tx_data.get('hash'),
                        type=OperationType.TRANSACTION,
                        direction=OperationDirection.INCOMING,
                        raw={},
                        confirmed=None,
                    )
                ],
                raw=tx,
            )

        if outgoing:
            return TransactionItem.from_api(
                fee_raw=tx.get('fee'),
                coin=self.coin,
                date=tx.get('created'),
                hash=outgoing.get('hash'),
                status=TransactionStatus.CONFIRMED,
                operations=[
                    OperationItem.from_api(
                        amount_raw=outgoing.get('value'),
                        coin=self.coin,
                        from_address=address,
                        to_address=(
                            tx['outputs'][0]['recipient']
                            if tx_data['output_count'] == 1
                            else 'multiple'
                        ),
                        hash=tx_data.get('hash'),
                        type=OperationType.TRANSACTION,
                        direction=OperationDirection.OUTGOING,
                        raw={},
                        confirmed=None,
                    )
                ],
                raw=tx,
            )


class BlockchairBitcoinApi(BlockchairApi):
    coin = COIN_BTC
    blockchain = Blockchain.BITCOIN
    name = 'bitcoin'
