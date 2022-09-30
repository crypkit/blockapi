from datetime import datetime

import pytz

from blockapi.services import AddressNotExist, BlockchainAPI, set_default_args_values


class BlockchainInfoAPI(BlockchainAPI):
    """
    Bitcoin
    API docs: https://www.blockchain.com/api/blockchain_api
    Explorer: https://blockchain.info
    """

    active = True

    symbol = 'BTC'
    base_url = 'https://blockchain.info'
    rate_limit = 0
    coef = 1e-8
    max_items_per_page = 100
    page_offset_step = max_items_per_page
    confirmed_num = 6

    supported_requests = {
        'get_balance': '/balance?active={address}',
        'get_txs': '/multiaddr?active={address}&n={number}&offset={offset}',
    }

    def process_error_response(self, response):
        if response.text == 'Invalid Bitcoin Address':
            raise AddressNotExist()
        # else
        super().process_error_response(response)

    def get_balance(self):
        balance = self.request('get_balance', address=self.address)
        if not balance:
            return None
        retval = list(balance.values())[0]['final_balance'] * self.coef
        return [{'symbol': self.symbol, 'amount': retval}]

    @set_default_args_values
    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        # always returns confimed transactions
        response = self.request(
            'get_txs', address=self.address, number=limit, offset=offset
        )
        return [self.parse_tx(t) for t in response['txs']]

    def parse_tx(self, tx):
        out_addresses = [o['addr'] for o in tx['out']]
        in_addresses = [i['prev_out']['addr'] for i in tx['inputs']]
        is_incoming = next((True for o in tx['out'] if o.get('xpub')), False)
        is_outgoing = next(
            (True for i in tx['inputs'] if i['prev_out'].get('xpub')), False
        )
        direction = 'incoming' if is_incoming else 'outgoing'

        if is_outgoing:
            from_addresses = in_addresses
            to_addresses = out_addresses
        else:
            from_addresses = out_addresses
            to_addresses = in_addresses

        return {
            'date': datetime.fromtimestamp(tx['time'], pytz.utc),
            'from_address': from_addresses,
            'to_address': to_addresses,  # multiple, TODO check it
            'amount': tx['balance'] * self.coef,
            'fee': tx['fee'] * self.coef,
            'hash': tx['hash'],
            'confirmed': None,
            'is_error': False,
            'type': 'normal',
            'kind': 'transaction',
            'direction': direction,
            'status': 'confirmed',
            'raw': tx,
        }
