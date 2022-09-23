from datetime import datetime

import pytz

from blockapi.services import AddressNotExist, BlockchainAPI, set_default_args_values


class DcrdataAPI(BlockchainAPI):
    """
    Decred
    API docs: https://github.com/decred/dcrdata#dcrdata-api
    Explorer: https://explorer.dcrdata.org
    """

    symbol = 'DCR'
    base_url = 'https://explorer.dcrdata.org/api'
    testnet_url = 'https://testnet.dcrdata.org/api'
    rate_limit = 0
    coef = 1
    max_items_per_page = 50000
    page_offset_step = max_items_per_page

    supported_requests = {
        'get_balance': '/address/{address}/totals',
        'get_transaction': '/tx/{tx_hash}?spends=true',
        'get_txs': '/address/{address}/count/{count}/skip/{skip}/raw',
    }

    def process_error_response(self, response):
        if response.status_code == 422:
            raise AddressNotExist()
        # else
        super().process_error_response(response)

    def get_balance(self):
        balance = self.request('get_balance', address=self.address)
        return [{'symbol': self.symbol, 'amount': balance['dcr_unspent']}]

    @set_default_args_values
    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        txs = self.request('get_txs', address=self.address, count=limit, skip=offset)
        return [self.parse_tx(tx) for tx in txs]

    def get_tx(self, tx_hash):
        """Despite the name this method is not returning single tx
        but might result in the array of txs
        """
        tx = self.request('get_transaction', tx_hash=tx_hash)
        return self.parse_tx(tx)['result']

    def parse_tx(self, tx):
        kind = self.get_tx_kind(tx)

        parsed = {
            'transaction': self.parse_regular_tx,
            'ticket': self.parse_ticket,
            'vote': self.parse_vote,
            'revocation': self.parse_revocation,
        }.get(kind)(tx)
        return {'kind': kind, 'result': parsed}

    @staticmethod
    def get_tx_kind(tx):
        tx_types = [t['scriptPubKey']['type'] for t in tx['vout']]
        if 'stakesubmission' in tx_types:  # and 'sstxcommitment', 'sstxchange'
            return 'ticket'
        elif 'stakegen' in tx_types:
            return 'vote'
        elif 'stakerevoke' in tx_types:
            return 'revocation'
        elif 'pubkeyhash' in tx_types:
            return 'transaction'  # 'regular' in api
        return None

    def parse_regular_tx(self, tx):
        # Tx in decred could contain several addresses, filter only mine
        ins = [
            v
            for v in tx['vin']
            if self.address in v.get('prevOut', {}).get('addresses', [])
        ]
        outs = [
            o
            for o in tx['vout']
            if self.address in o.get('scriptPubKey', {}).get('addresses', [])
        ]

        # get_txs has time attribute, get_tx has block.time attribute
        if 'time' in tx:
            date = datetime.fromtimestamp(tx['time'], pytz.utc)
        else:
            date = datetime.fromtimestamp(tx['block']['time'], pytz.utc)

        parsed = []
        for i in ins:
            parsed.append(
                {
                    'date': date,
                    'from_address': self.address,
                    'to_address': None,  # multiple, TODO check it
                    'amount': i['amountin'],
                    'fee': None,
                    'gas_limit': None,
                    'hash': tx['txid'],
                    'confirmed': tx['confirmations'] > self.confirmed_num,
                    'is_error': False,
                    'type': 'normal',
                    'kind': 'transaction',
                    'direction': 'outgoing',
                    'status': None,
                    'raw': tx,
                }
            )

        for o in outs:
            parsed.append(
                {
                    'date': date,
                    'from_address': None,  # multiple, TODO check it
                    'to_address': self.address,
                    'amount': o['value'],
                    'fee': None,
                    'gas_limit': None,
                    'hash': tx['txid'],
                    'confirmed': tx['confirmations'] > self.confirmed_num,
                    'is_error': False,
                    'type': 'normal',
                    'kind': 'transaction',
                    'direction': 'incoming',
                    'status': None,
                    'raw': tx,
                }
            )
        return parsed

    @staticmethod
    def parse_ticket(tx):
        investment = sum(v['amountin'] for v in tx['vin'])
        ticket_cost = next(
            (
                v['value']
                for v in tx['vout']
                if v['scriptPubKey']['type'] == 'stakesubmission'
            ),
            0,
        )

        # pool fee is lower value then ticket cost,
        # but not sure if it's correct
        pool_fee = min([v['amountin'] for v in tx['vin']]) if len(tx['vin']) > 1 else 0

        return {
            'hash': tx['txid'],
            'purchased_on': datetime.fromtimestamp(tx['time'], pytz.utc),
            # all input tx ids in tx['vin'] should be same?
            'input_tx_id': tx['vin'][0]['txid'],
            'investment': investment,
            'ticket_cost': ticket_cost,
            'transaction_fee': investment - ticket_cost,
            'pool_fee': pool_fee,
            'block_hash': tx['blockhash'],
            'block_height': None,  # TODO
            'status': DcrdataAPI.get_ticket_status(tx),
        }

    @staticmethod
    def get_ticket_status(tx):
        # params for mainnet:
        # https://github.com/decred/dcrd/blob
        # /9da132b9823b20870122dc0bf795884cee99d922
        # /chaincfg/mainnetparams.go#L321
        if tx['confirmations'] < 1:
            return 'unmined'
        elif tx['confirmations'] < 256:
            return 'immature'
        # TODO - not sure about this one
        elif tx['confirmations'] < 7640:
            return 'live'
        elif tx['confirmations'] < 40960:
            return 'voted'
        elif tx['confirmations'] > 40960:
            return 'expired'

        # other statuses depends on specific txs
        # (votes -> voted, revocations -> revocated)
        # -> specific tx refers to ticket by ticket_hash
        # otherwise is live
        return 'live'

    @staticmethod
    def parse_vote(tx):
        total_input = 0
        reward = 0
        ticket_hash = None
        for v in tx['vin']:
            if 'stakebase' in v:
                reward = v['amountin']
                total_input += reward
            else:
                # value of ticket
                ticket_hash = v['txid']
                total_input += v['prevOut']['value']

        total_output = sum(v['value'] for v in tx['vout'] if v['value'])

        return {
            'hash': tx['txid'],
            'voted_on': datetime.fromtimestamp(tx['time'], pytz.utc),
            'spent_ticket_hash': ticket_hash,
            'reward': reward,
            'fee': total_input - total_output,
            'block_hash': tx['blockhash'],
        }

    @staticmethod
    def parse_revocation(tx):
        ticket_hash = next((v['txid'] for v in tx['vin']), None)
        total_input = sum(v['amountin'] for v in tx['vin'] if v['amountind'])
        total_output = sum(v['value'] for v in tx['vout'] if v['value'])

        return {
            'hash': tx['txid'],
            'revocated_on': datetime.fromtimestamp(tx['time'], pytz.utc),
            'spent_ticket_hash': ticket_hash,
            'fee': total_input - total_output,
            'block_hash': tx['blockhash'],
        }
