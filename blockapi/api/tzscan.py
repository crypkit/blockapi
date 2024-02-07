import dateutil.parser

from blockapi.services import APIError, BlockchainAPI, set_default_args_values


class TzscanAPI(BlockchainAPI):
    """
    Tezos
    API docs: https://tzscan.io/api
        Explorer: https://tzscan.io
    """

    # inaccurate results for balances, use on your own risk
    active = False

    symbol = 'XTZ'
    base_url = None  # endpoint is created in runtime
    rate_limit = 0
    coef = 1e-6
    max_items_per_page = 50
    page_offset_step = 1

    supported_requests = {
        'get_balance': '/v3/balance_from_balance_updates/{address}',
        'get_operations': '/v3/operations/{address}'
        '?type={type}&p={page_offset}&number={number}',
        'get_rewards': '/v3/rewards_split_cycles/{address}'
        '?p={page_offset}&number={number}',
        'get_rewards_split': '/v2/rewards_split/{address}'
        '?cycle={cycle}&number=50&p={page}',
        'get_bakings': '/v3/cycle_bakings/{address}' '?p={page_offset}&number={number}',
        'get_endorsements': '/v3/cycle_endorsements/{address}'
        '?p={page_offset}&number={number}',
    }

    def __init__(self, address, *args, **kwargs):
        super().__init__(address)
        # this API is very unstable, add some functionality to prevent fails
        self._base_url_temp = 'https://api{num}.dunscan.io'  # num is 1-6
        self._api_nums = [1, 2, 3, 4, 5, 6]

    def get_balance(self):
        balance = self._safe_request('get_balance', address=self.address)
        return [
            {'symbol': self.symbol, 'amount': float(balance['spendable']) * self.coef}
        ]

    def get_rewards(self, offset=0, limit=50):
        rewards = self._safe_request(
            'get_rewards', address=self.address, page_offset=offset, number=limit
        )

        return [
            self.get_reward_details(reward, int(reward['cycle'])) for reward in rewards
        ]

    def get_reward_details(self, reward_v3, cycle=None):
        reward = self._safe_request(
            'get_rewards_split', address=self.address, cycle=cycle, page=0
        )

        total_staking_balance = float(reward['delegate_staking_balance'])
        total_rewards = (
            float(reward['blocks_rewards'])
            + float(reward['endorsements_rewards'])
            + float(reward['fees'])
            + float(reward['future_blocks_rewards'])
            + float(reward['future_endorsements_rewards'])
            + float(reward['gain_from_denounciation_baking'])
            + float(reward['revelation_rewards'])
            + float(reward['gain_from_denounciation_endorsement'])
            - float(reward['lost_deposit_from_denounciation_baking'])
            - float(reward['lost_fees_denounciation_baking'])
            - float(reward['lost_rewards_denounciation_baking'])
            - float(reward['lost_deposit_from_denounciation_endorsement'])
            - float(reward['lost_fees_denounciation_endorsement'])
            - float(reward['lost_rewards_denounciation_endorsement'])
            - float(reward['lost_revelation_rewards'])
            - float(reward['lost_revelation_fees'])
        )

        total_staking_balance = round(float(total_staking_balance) / 1000000, 6)
        total_delegators = int(reward['delegators_nb'])
        pages = total_delegators / 50

        delegations = []
        delegators = 0
        page = 0

        while True:
            for del_balance in reward['delegators_balance']:
                delegator_address = del_balance[0]['tz']
                delegator_balance = int(del_balance[1]) * self.coef
                share = float(delegator_balance) / total_staking_balance
                delegations.append(
                    {
                        'address': delegator_address,
                        'balance': delegator_balance,
                        'share': share * 100,
                        'rewards_share': share * (total_rewards * self.coef),
                    }
                )
                delegators += 1

            page += 1
            if page < pages:
                reward = self._safe_request(
                    'get_rewards_split', address=self.address, cycle=cycle, page=page
                )
            else:
                break

        return {
            'staking_balance': total_staking_balance,
            'cycle': cycle,
            'status': reward_v3['status']['status'],
            'delegators': delegators,
            'delegations': delegations,
            'end_rewards': float(reward['endorsements_rewards']) * self.coef,
            'blocks_rewards': float(reward['blocks_rewards']) * self.coef,
            'extra_rewards': float(reward['revelation_rewards']) * self.coef,
            'losses': float(reward['lost_revelation_rewards']) * self.coef,
            'fees': float(reward['fees']) * self.coef,
        }

    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        return self._get_operations('Transaction', self.parse_tx, offset, limit)

    def get_activations(self, offset=None, limit=None):
        return self._get_operations('Activation', self.parse_activation, offset, limit)

    def get_originations(self, offset=None, limit=None):
        return self._get_operations(
            'Origination', self.parse_origination, offset, limit
        )

    def get_delegations(self, offset=None, limit=None):
        return self._get_operations('Delegation', self.parse_delegation, offset, limit)

    @set_default_args_values
    def _get_operations(self, op_type, parse, offset=None, limit=None):
        """Get all operations by type
        @op_type in [Transaction, Origination, Delegation, Activation, ...]"""

        operations = self._safe_request(
            'get_operations',
            address=self.address,
            type=op_type,
            page_offset=offset,
            number=limit,
        )

        parsed_txs = []
        for tx in operations:
            parsed_txs += parse(tx)
        return parsed_txs

    def parse_tx(self, tx):
        # tezos can have multiple txs in single tx (with one hash)
        parsed = []
        for op in tx.get('type', {}).get('operations', []):
            parsed.append(
                {
                    'date': dateutil.parser.parse(op['timestamp']),
                    'from_address': op['src']['tz'],
                    'to_address': op['destination']['tz'],
                    'amount': float(op['amount']) * self.coef,
                    'fee': (
                        None if float(op['fee']) == -1 else float(op['fee']) * self.coef
                    ),
                    'gas_limit': (
                        None if int(op['gas_limit']) == -1 else int(op['gas_limit'])
                    ),
                    'hash': tx['hash'],
                    'confirmed': None,
                    'is_error': op['failed'],
                    'type': 'internal' if op['internal'] else 'normal',
                    'kind': op['kind'].lower(),
                    'direction': (
                        'outgoing' if self.address == op['src']['tz'] else 'incoming'
                    ),
                    'raw': tx,
                }
            )
            return parsed

    def parse_delegation(self, tx):
        parsed = []
        for op in tx.get('type', {}).get('operations', []):
            parsed.append(
                {
                    'date': dateutil.parser.parse(op['timestamp']),
                    'source_address': op['src']['tz'],
                    'delegate': op['delegate']['tz'],
                    'fee': None if op['fee'] == -1 else op['fee'] * self.coef,
                    'gas_limit': (
                        None if int(op['gas_limit']) == -1 else int(op['gas_limit'])
                    ),
                    'hash': tx['hash'],
                    'is_error': op['failed'],
                    'type': 'internal' if op['internal'] else 'normal',
                    'kind': op['kind'].lower(),
                    'raw': tx,
                }
            )
            return parsed

    @staticmethod
    def parse_activation(tx):
        parsed = []
        for op in tx.get('type', {}).get('operations', []):
            parsed.append(
                {
                    'date': dateutil.parser.parse(op['timestamp']),
                    'secret': op['secret'],
                    'balance': op['balance'],
                    'hash': tx['hash'],
                    'kind': op['kind'].lower(),
                    'raw': tx,
                }
            )
            return parsed

    def parse_origination(self, tx):
        parsed = []
        for op in tx.get('type', {}).get('operations', []):
            parsed.append(
                {
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
                    'gas_limit': (
                        None if int(op['gas_limit']) == -1 else int(op['gas_limit'])
                    ),
                    'hash': tx['hash'],
                    'is_error': op['failed'],
                    'type': 'internal' if op['internal'] else 'normal',
                    'kind': op['kind'].lower(),
                    'raw': tx,
                }
            )
            return parsed

    @set_default_args_values
    def get_endorsements(self, offset=None, limit=None):
        ends = self._safe_request(
            'get_endorsements', address=self.address, page_offset=offset, number=limit
        )
        return [self.parse_endorsement(e) for e in ends]

    def parse_endorsement(self, e):
        return {
            'cycle': int(e['cycle']),
            'depth': int(e['depth']),
            'num_slots': {
                'all': int(e['slots']['count_all']),
                'miss': int(e['slots']['count_miss']),
                'steal': int(e['slots']['count_steal']),
            },
            'fee': int(e['tez']['fee']) * self.coef,
            'reward': int(e['tez']['reward']) * self.coef,
            'deposit': int(e['tez']['deposit']) * self.coef,
            'priority': float(e['priority']),
        }

    @set_default_args_values
    def get_bakings(self, offset=None, limit=None):
        baks = self._safe_request(
            'get_bakings', address=self.address, page_offset=offset, number=limit
        )
        return [self.parse_baking(b) for b in baks]

    def parse_baking(self, b):
        return {
            'cycle': int(b['cycle']),
            'depth': int(b['depth']),
            'num_blocks': {
                'all': int(b['count']['count_all']),
                'miss': int(b['count']['count_miss']),
                'steal': int(b['count']['count_steal']),
            },
            'fee': int(b['tez']['fee']) * self.coef,
            'reward': int(b['tez']['reward']) * self.coef,
            'deposit': int(b['tez']['deposit']) * self.coef,
            'priority': float(b['priority']),
            'bake_time': int(b['bake_time']),
        }

    def _safe_request(self, method, **params):
        api_nums = self._api_nums.copy()
        ex = Exception('Runtime error')

        while api_nums:
            try:
                api_num = api_nums.pop(0)
                self.base_url = self._base_url_temp.format(num=api_num)
                response = self.request(method, **params)
            except APIError as e:
                ex = e
                continue
            else:
                return response

        # when all endpoints are checked and none of them is valid, raise exc
        raise ex
