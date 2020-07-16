from decimal import Decimal

from blockapi.services import BlockchainAPI


class TerraMoneyApi(BlockchainAPI):
    """
    Terra Money
    API docs: UNKNOWN
    Explorer: https://fcd.terra.dev/
    """

    symbol = 'LUNA'
    base_url = 'https://fcd.terra.dev/v1'
    rate_limit = 0.5
    coef = Decimal(1e-6)
    max_items_per_page = 50
    page_offset_step = 1

    supported_requests = {
        'get_balance': '/bank/{address}',
        'get_delegations': '/staking/{address}',
        'get_txs': '/txs?account={address}&limit={limit}&page={page}'
    }

    symbols = {
        'uluna': 'LUNA',
        'ukrw': 'KRT',
        'usdr': 'SDT',
        'uusd': 'UST',
        'umnt': 'MNT'
    }

    tx_kinds = {
        'bank/MsgSend': 'deposit',
        'staking/MsgDelegate': 'delegation',
        'distribution/MsgWithdrawDelegationReward': 'delegation_withdrawal'
    }

    def get_balance(self):
        balances = self.request('get_balance', address=self.address)
        if not balances:
            return None

        return_balances = []
        for bal in balances['balance']:
            return_balances.append({
                'symbol': self._get_symbol(bal['denom']),
                'amount': Decimal(bal['available']) * self.coef
            })

        # Add staked amount in LUNA
        for delegation in balances['delegations']:
            luna = next((b for b in return_balances if b['symbol'] == 'LUNA'),
                        {'symbol': 'LUNA', 'amount': 0})
            luna['amount'] += Decimal(delegation['amount']) * self.coef

        return return_balances

    def get_txs(self, offset=1, limit=1000, unconfirmed=False):
        txs_req = self.request('get_txs', address=self.address, limit=limit,
                               page=offset)
        if not txs_req:
            return None

        txs = []
        for tx in txs_req['txs']:
            tx_item = {
                'kind': self.tx_kinds.get(tx['tx']['value']['msg'][0]['type']),
                'result': self.parse_tx(tx)
            }
            txs.append(tx_item)

        return txs

    def get_delegations(self):
        delegations = self.request('get_delegations', address=self.address)

        # Convert all numbers
        return self._load(delegations)

    def parse_tx(self, tx):
        fee = tx['tx']['value']['fee']
        msg = tx['tx']['value']['msg']
        return {
            'date': tx['timestamp'],
            'fee': [{
                'symbol': self._get_symbol(f['denom']),
                'amount': Decimal(f['amount']) * self.coef
            } for f in fee['amount']],
            'amount': [self.parse_tx_amount(m['value'])for m in msg]
        }

    def parse_tx_amount(self, tx_value):

        if 'amount' not in tx_value:
            return None

        tx_amount = tx_value['amount']
        if isinstance(tx_amount, list):
            amount = [{
                'symbol': self._get_symbol(t['denom']),
                'amount': Decimal(t['amount']) * self.coef
            } for t in tx_amount]
        else:
            amount = {
                'symbol': self._get_symbol(tx_amount['denom']),
                'amount': Decimal(tx_amount['amount']) * self.coef
            }
        return amount

    @classmethod
    def _get_symbol(cls, denom):
        """It seems that API returns only denom instead of correct
        symbols.
        """
        return cls.symbols.get(denom, 'unknown')
