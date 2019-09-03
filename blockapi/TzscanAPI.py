import dateutil.parser
import random
from .services import BlockchainAPI,set_default_args_values,APIError,AddressNotExist,BadGateway,GatewayTimeOut

class TzscanAPI(BlockchainAPI):
    """
    Tezos
    API docs: https://tzscan.io/api
    Explorer: https://tzscan.io
    """

    currency_id = 'tezos'
    _base_url = 'https://api{num}.tzscan.io' # num = 1-6
    rate_limit = 0
    coef = 1e-6
    max_items_per_page = 50
    page_offset_step = 1

    supported_requests = {
        'get_balance': '/v3/balance_from_balance_updates/{address}',
        'get_operations': '/v3/operations/{address}?type={type}&p={page_offset}&number={number}',
        'get_rewards': '/v3/rewards_split_cycles/{address}?p={page_offset}&number={number}',
        'get_bakings': '/v3/cycle_bakings/{address}?p={page_offset}&number={number}',
        'get_endorsements': '/v3/cycle_endorsements/{address}?p={page_offset}&number={number}'
    }

    @property
    def base_url(self):
        return self._base_url.format(num=random.randint(1, 6))

    def get_balance(self):
        balance = self.request('get_balance', address=self.address)
        return float(balance['spendable']) * self.coef

    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        return self._get_operations(
            'Transaction', self.parse_tx, offset, limit)

    def get_activations(self, offset=None, limit=None, unconfirmed=False):
        return self._get_operations(
            'Activation', self.parse_activation, offset, limit)

    def get_originations(self, offset=None, limit=None, unconfirmed=False):
        return self._get_operations(
            'Origination', self.parse_origination, offset, limit)

    def get_delegations(self, offset=None, limit=None, unconfirmed=False):
        return self._get_operations(
            'Delegation', self.parse_delegation, offset, limit)

    @set_default_args_values
    def _get_operations(self, op_type, parse, offset=None, limit=None):
        """Get all operations by type
        @op_type in [Transaction, Origination, Delegation, Activation, ...]"""

        operations = self.request(
            'get_operations',
            address=self.address,
            type=op_type,
            page_offset=offset,
            number=limit
        )

        parsed_txs = []
        for tx in operations:
            parsed_txs += parse(tx)
        return parsed_txs

    def parse_tx(self, tx):
        # tezos can have multiple txs in single tx (with one hash)
        parsed = []
        for op in tx.get('type', {}).get('operations', []):
            parsed.append({
                'date': dateutil.parser.parse(op['timestamp']),
                'from_address': op['src']['tz'],
                'to_address': op['destination']['tz'],
                'amount': float(op['amount']) * self.coef,
                'fee': None if op['fee'] == -1 else op['fee'] * self.coef,
                'gas_limit': None if int(op['gas_limit']) == -1 else int(op['gas_limit']),
                'hash': tx['hash'],
                'confirmed': None,
                'is_error': op['failed'],
                'type': 'internal' if op['internal'] else 'normal',
                'kind': op['kind'].lower(),
                'direction': 'outgoing' if self.address == op['src']['tz'] else 'incoming',
                'raw': tx
            })
            return parsed

    def parse_delegation(self, tx):
        parsed = []
        for op in tx.get('type', {}).get('operations', []):
            parsed.append({
                'date': dateutil.parser.parse(op['timestamp']),
                'source_address': op['src']['tz'],
                'delegate': op['delegate']['tz'],
                'fee': None if op['fee'] == -1 else op['fee'] * self.coef,
                'gas_limit': None if int(op['gas_limit']) == -1 else int(op['gas_limit']),
                'hash': tx['hash'],
                'is_error': op['failed'],
                'type': 'internal' if op['internal'] else 'normal',
                'kind': op['kind'].lower(),
                'raw': tx
            })
            return parsed

    def parse_activation(self, tx):
        parsed = []
        for op in tx.get('type', {}).get('operations', []):
            parsed.append({
                'date': dateutil.parser.parse(op['timestamp']),
                'secret': op['secret'],
                'balance': op['balance'],
                'hash': tx['hash'],
                'kind': op['kind'].lower(),
                'raw': tx
            })
            return parsed

    def parse_origination(self, tx):
        parsed = []
        for op in tx.get('type', {}).get('operations', []):
            parsed.append({
                'date': dateutil.parser.parse(op['timestamp']),
                'originator': op['src']['tz'],
                'manager': op['managerPubkey']['tz'],
                'balance': op['balance'],
                'spendable': op['spendable'],
                'delegatable': op['delegatable'],
                'delegate': op['delegate']['tz'],
                'delegate_alias': op['delegate']['alias'],
                'burnt': op['burn_tez'] * self.coef,
                'fee': None if op['fee'] == -1 else op['fee'] * self.coef,
                'gas_limit': None if int(op['gas_limit']) == -1 else int(op['gas_limit']),
                'hash': tx['hash'],
                'is_error': op['failed'],
                'type': 'internal' if op['internal'] else 'normal',
                'kind': op['kind'].lower(),
                'raw': tx
            })
            return parsed


    @set_default_args_values
    def get_endorsements(self, offset=None, limit=None):
        ends = self.request(
            'get_endorsements',
            address=self.address,
            page_offset=offset,
            number=limit
        )
        return [self.parse_endorsement(e) for e in ends]

    def parse_endorsement(self, e):
        return {
            'cycle': int(e['cycle']),
            'depth': int(e['depth']),
            'num_slots': {
                'all': int(e['slots']['count_all']),
                'miss': int(e['slots']['count_miss']),
                'steal': int(e['slots']['count_steal'])
            },
            'fee': int(e['tez']['fee']) * self.coef,
            'reward': int(e['tez']['reward']) * self.coef,
            'deposit': int(e['tez']['deposit']) * self.coef,
            'priority': float(e['priority'])
        }

    @set_default_args_values
    def get_bakings(self, offset=None, limit=None):
        baks = self.request(
            'get_bakings',
            address=self.address,
            page_offset=offset,
            number=limit
        )
        return [self.parse_baking(b) for b in baks]

    def parse_baking(self, b):
        return {
            'cycle': int(b['cycle']),
            'depth': int(b['depth']),
            'num_blocks': {
                'all': int(b['count']['count_all']),
                'miss': int(b['count']['count_miss']),
                'steal': int(b['count']['count_steal'])
            },
            'fee': int(b['tez']['fee']) * self.coef,
            'reward': int(b['tez']['reward']) * self.coef,
            'deposit': int(b['tez']['deposit']) * self.coef,
            'priority': float(b['priority']),
            'bake_time': int(b['bake_time'])
        }
