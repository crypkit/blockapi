from datetime import datetime

import pytz

from blockapi.services import BlockchainAPI


class TrezorAPI(BlockchainAPI):
    """
    coins: bitcoin, litecoin
    API docs: https://github.com/trezor/blockbook/blob/master/docs/api.md
    Explorer:
    """

    active = True

    rate_limit = 0
    coef = 1e-8
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None
    xpub_support = True

    supported_requests = {
        'get_balance': '/api/v2/address/{address}',
        'get_balance_xpub': '/api/v2/xpub/{address}',
        'get_txs': '/api/v2/utxo/{address}?confirmed={confirmed}',
        'get_tx': '/api/v2/tx/{tx_hash}',
    }

    def get_balance(self):
        if len(self.address) == 111:
            response = self.request('get_balance_xpub', address=self.address)
        else:
            response = self.request('get_balance', address=self.address)

        if not response:
            return None

        retval = float(response.get('balance')) * self.coef
        return [{'symbol': self.symbol, 'amount': retval}]

    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        response = self.request(
            'get_txs', address=self.address, confirmed=not unconfirmed
        )

        return [self.parse_tx(tx) for tx in response]

    def parse_tx(self, tx):
        txdata = self.request('get_tx', tx_hash=tx['txid'])

        if self.address in txdata['vin'][0]['addresses']:
            direction = 'outgoing'
        else:
            direction = 'incoming'

        return {
            'date': datetime.fromtimestamp(txdata['blockTime'], pytz.utc),
            'from_address': txdata['vin'][0]['addresses'],
            'to_address': txdata['vout'][0]['addresses'],
            'amount': float(txdata['value']) * self.coef,
            'fee': float(txdata['fees']) * self.coef,
            'hash': tx['txid'],
            'confirmed': txdata['confirmations'],
            'is_error': False,
            'type': 'normal',
            'kind': 'transaction',
            'direction': direction,
            'status': 'confirmed' if txdata['confirmations'] > 0 else 'unconfirmed',
            'raw': txdata,
        }


class Btc1TrezorAPI(TrezorAPI):
    base_url = 'https://btc1.trezor.io'
    symbol = 'BTC'


class Btc2TrezorAPI(TrezorAPI):
    base_url = 'https://btc2.trezor.io'
    symbol = 'BTC'


class Ltc1TrezorAPI(TrezorAPI):
    base_url = 'https://ltc1.trezor.io'
    symbol = 'LTC'
