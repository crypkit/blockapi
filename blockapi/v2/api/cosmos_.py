import re
from copy import deepcopy

import dateutil.parser

from blockapi.services import (
    AddressNotExist,
    APIError,
    BlockchainAPI,
    set_default_args_values,
)


class CosmosAPI(BlockchainAPI):
    """
    Cosmos
    API docs: https://cosmos.network/rpc/
    Explorer: https://www.mintscan.io
    """

    symbol = 'ATOM'
    # base_url is 'https://stargate.cosmos.network'
    base_url = 'https://cosmos.node.cracklord.com'
    rate_limit = 0.6
    coef = 1e-6
    start_offset = 1
    max_items_per_page = 30
    page_offset_step = 1

    supported_requests = {
        'get_info': '/auth/accounts/{address}',
        'get_balance': '/bank/balances/{address}',
        'get_txs': '/txs?action={action}&{role}={address}&page={page}' '&limit={limit}',
        'get_delegations': '/staking/delegators/{address}/delegations',
        'get_unbonding_delegations': '/staking/delegators/{address}'
        '/unbonding_delegations',
        'get_redelegations': '/staking/redelegations?delegator={address}',
        'get_delegation_reward': '/distribution/delegators/{address}'
        '/rewards/{validator_address}',
        'get_proposals': '/gov/proposals',
        'query_votes': '/gov/proposals/{proposal_id}/votes',
    }

    def process_error_response(self, response):
        if 'decoding bech32 failed' in response.text:
            raise AddressNotExist()
        # else
        super().process_error_response(response)

    def get_info(self):
        return self.request('get_info', address=self.address)

    def get_balance(self):
        balances = self.request('get_balance', address=self.address)
        if not balances:
            return None

        balances_result = []
        for b in balances['result']:
            symbol = self.symbol if b['denom'] == 'uatom' else b['denom']
            balances_result.append(
                {'symbol': symbol, 'amount': int(b['amount']) * self.coef}
            )
        return balances_result

    def get_delegations(self):
        return self.request('get_delegations', address=self.address)

    def get_unbonding_delegations(self):
        return self.request('get_unbonding_delegations', address=self.address)

    def get_redelegations(self):
        return self.request('get_redelegations', address=self.address)

    def get_delegation_reward(self, validator_address):
        return self.request(
            'get_delegation_reward',
            address=self.address,
            validator_address=validator_address,
        )

    def get_proposals(self):
        return self.request('get_proposals')

    def get_votes_deprecated(self):
        votes = []
        for prop in self.get_proposals():
            try:
                vote = self.request('query_votes', proposal_id=prop['proposal_id'])
                if vote is None:
                    continue
                for v in vote:
                    if v['voter'] == self.address:
                        votes.append(v)

            except APIError:
                pass

        return votes

    def get_incoming_txs(self, offset=None, limit=None, unconfirmed=False):
        txs = self._get_txs('send', 'recipient', offset, limit, unconfirmed)
        return self.parse_txs(txs)

    def get_outgoing_txs(self, offset=None, limit=None, unconfirmed=False):
        txs = self._get_txs('send', 'sender', offset, limit, unconfirmed)
        return self.parse_txs(txs)

    def get_multi_incoming_txs(self, offset=None, limit=None, unconfirmed=False):
        txs = self._get_txs('multisend', 'recipient', offset, limit, unconfirmed)
        return self.parse_txs(txs)

    def get_multi_outgoing_txs(self, offset=None, limit=None, unconfirmed=False):
        txs = self._get_txs('multisend', 'sender', offset, limit, unconfirmed)
        return self.parse_txs(txs)

    def parse_txs(self, txs):
        parsed_txs = []
        for tx in txs['txs']:
            # there can be multiple txs in single tx
            for parsed in self.parse_tx(tx):
                parsed_txs.append(parsed)
        return parsed_txs

    def parse_tx(self, tx):
        fee_amount = int(tx['tx']['value']['fee']['amount'][0]['amount'])
        base_tx = {
            'date': dateutil.parser.parse(tx['timestamp']),
            'fee': fee_amount * self.coef if fee_amount else None,
            'gas': {
                'gas_used': int(tx['gas_used']),
                'gas_limit': int(tx['gas_wanted']),
            },
            'hash': tx['txhash'],
            'confirmed': None,
            'type': 'normal',
            'kind': 'transaction',
            'description': tx['tx']['value']['memo'],
            'raw': tx,
        }

        # for every message (sub tx?) create new tx
        msgs = []
        for msg in self._parse_messages(tx):
            msg['direction'] = (
                'incoming'
                if msg['to_address'].lower() == self.address.lower()
                else 'outgoing'
            )
            msg.update(base_tx)
            msgs.append(msg)
        return msgs

    #
    def get_rewards_withdrawals(self, offset=None, limit=None):
        items = self._get_txs('withdraw_delegator_reward', 'delegator', offset, limit)
        return self.parse_other_txs(items)

    #
    def get_redelegates(self, offset=None, limit=None):
        items = self._get_txs('begin_redelegate', 'delegator', offset, limit)
        return self.parse_other_txs(items)

    #
    def get_delegates(self, offset=None, limit=None):
        items = self._get_txs('delegate', 'delegator', offset, limit)
        return self.parse_other_txs(items)

    #
    def get_undelegates(self, offset=None, limit=None):
        items = self._get_txs('begin_unbonding', 'delegator', offset, limit)
        return self.parse_other_txs(items)

    def get_votes(self, offset=None, limit=None):
        items = self._get_txs('vote', 'voter', offset, limit)
        return self.parse_other_txs(items)

    # only for validators
    def get_validator_edits(self, offset=None, limit=None):
        items = self._get_txs('edit_validator', 'destination-validator', offset, limit)
        return self.parse_other_txs(items)

    # create validator
    # https://stargate.cosmos.network/txs/938AFA947B6EBE4CA614FFD7C8F98F2452
    # 8A395061FAC68EF1EFB92422F6158F

    def parse_other_txs(self, txs):
        parsed_txs = []
        for tx in txs:
            # there can be multiple txs in single tx
            for parsed in self._parse_other_tx(tx):
                parsed_txs.append(parsed)
        return parsed_txs

    @set_default_args_values
    def _get_txs(self, action, role, offset=None, limit=None, unconfirmed=None):
        return self.request(
            'get_txs',
            action=action,
            role=role,
            address=self.address,
            page=offset,
            limit=limit,
            unconfirmed=unconfirmed,
        )

    def _parse_other_tx(self, tx):
        fee_data = tx['tx']['value']['fee']['amount']
        fee_amount = int(fee_data[0]['amount']) * self.coef if fee_data else None

        base_tx = {
            'date': dateutil.parser.parse(tx['timestamp']),
            'fee': fee_amount,
            'gas': {
                'gas_used': int(tx['gas_used']),
                'gas_limit': int(tx['gas_wanted']),
            },
            'hash': tx['txhash'],
            'description': tx['tx']['value']['memo'],
            'raw': tx,
        }

        # for every message (sub tx?) create new tx
        msgs = []
        for msg in self._parse_messages(tx):
            _tx = deepcopy(base_tx)
            _tx['kind'] = msg.pop('kind')
            _tx['operation'] = msg
            msgs.append(_tx)
        return msgs

    def _parse_messages(self, tx):
        logs = deepcopy(tx['logs'])

        # only reward has values in separated dict
        r = re.compile("([0-9]+)([a-zA-Z]+)")
        # [($number, $coin), ...]
        rewards = [
            r.match(t['value']).groups() for t in tx['tags'] if t['key'] == 'rewards'
        ]

        parsed_msgs = []
        for msg in tx['tx']['value']['msg']:

            msg_type = self._convert_msg_kind(msg['type'])
            parsed_msg = self._get_msg_data(msg_type, msg['value'])

            if msg_type == 'reward':
                reward = rewards.pop(0) if rewards else None
                if reward:
                    parsed_msg['amount'] = int(reward[0]) * self.coef

            log = logs.pop(0)
            parsed_msg['is_error'] = not log['success']
            parsed_msg['kind'] = msg_type

            parsed_msgs.append(parsed_msg)

        return parsed_msgs

    @staticmethod
    def _convert_msg_kind(raw_type):
        return {
            'cosmos-sdk/MsgSend': 'transaction',
            'cosmos-sdk/MsgMultiSend': 'multisend',
            'cosmos-sdk/MsgWithdrawDelegationReward': 'reward',
            'cosmos-sdk/MsgDelegate': 'delegate',
            'cosmos-sdk/MsgBeginRedelegate': 'redelegate',
            'cosmos-sdk/MsgVote': 'vote',
        }.get(raw_type, raw_type)

    def _get_msg_data(self, msg_type, msg_value):
        # use original fields from api, change only amounts if needed
        msg_info = deepcopy(msg_value)

        if msg_type == 'reward':
            # amount for rewards are saved in different field,
            # see caller method
            pass

        elif msg_type == 'multisend':
            msg_result = self._process_msg_type_multisend(msg_value)
            if msg_result is not None:
                return msg_result
        else:
            amount_obj = msg_value['amount']
            amount_data = {}
            if isinstance(amount_obj, list):
                amount_data = amount_obj[0] if amount_obj else {}
            elif isinstance(amount_obj, dict):
                amount_data = amount_obj

            msg_info['amount'] = (
                int(amount_data['amount']) * self.coef if amount_data else None
            )

        return msg_info

    def _process_msg_type_multisend(self, msg_value):
        my_input = next(
            (
                i
                for i in msg_value['inputs']
                if i['address'].lower() == self.address.lower()
            ),
            None,
        )

        my_output = next(
            (
                i
                for i in msg_value['outputs']
                if i['address'].lower() == self.address.lower()
            ),
            None,
        )

        if my_input:
            to_address = (
                msg_value['outputs'][0]['address']
                if len(msg_value['outputs']) == 1
                else 'multiple'
            )
            return {
                'from_address': self.address,
                'to_address': to_address,
                'amount': int(my_input['coins'][0]['amount']) * self.coef,
            }
        if my_output:
            from_address = (
                msg_value['inputs'][0]['address']
                if len(msg_value['inputs']) == 1
                else 'multiple'
            )
            return {
                'from_address': from_address,
                'to_address': self.address,
                'amount': int(my_output['coins'][0]['amount']) * self.coef,
            }
