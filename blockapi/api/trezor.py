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
    _tokens = []

    supported_requests = {
        'get_address': '/api/v2/address/{address}?page={page}&pageSize={page_size}&details={details}&contract= \
                         {contract_address}',
        'get_xpub': '/api/v2/xpub/{address}?page={page}&pageSize={page_size}&details={details}&tokens={tokens}',
    }

    def get_balance(self):
        if len(self.address) == 111:
            response = self.request('get_xpub',
                                    address=self.address,
                                    page = None,
                                    page_size=None,
                                    details=None,
                                    tokens=None)
        else:
            response = self.request('get_address',
                                    address=self.address,
                                    page=None,
                                    page_size=None,
                                    details=None,
                                    contract_address=None)

        if not response:
            return None

        retval = float(response.get('balance')) * self.coef
        return [{'symbol': self.symbol, 'amount': retval}]

    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        if len(self.address) == 111:
            response = self.request('get_xpub',
                                address=self.address,
                                page=offset,
                                page_size=limit,
                                details='txs',
                                tokens='used')
            if not 'tokens' in response:
                return []
            if offset and int(response['totalPages']) < offset:
                return []
            self._tokens = [t['name'] for t in response['tokens']]

            return [self.parse_tx(tx) for tx in response['transactions']]
        else:
            return None

    def parse_tx(self, txdata):
        in_addrs = [a['addresses'][0] for a in txdata['vin']]
        out_addrs = [a['addresses'][0] for a in txdata['vout']]
        received = self._get_value_sum(out_addrs, txdata['vout'])

        if len(set(in_addrs) & set(self._tokens)):
            direction = 'outgoing'
            amount = self._get_value_sum(in_addrs, txdata['vin']) - received
        else:
            direction = 'incoming'
            amount = received

        return {
            'date': str(datetime.fromtimestamp(txdata['blockTime'], pytz.utc)),
            'from_address': in_addrs,
            'to_address': out_addrs,
            'amount': float(amount) * self.coef,
            'fee': float(txdata['fees']) * self.coef,
            'hash': txdata['txid'],
            'confirmed': txdata['confirmations'],
            'is_error': False,
            'type': 'normal',
            'kind': 'transaction',
            'direction': direction,
            'status': 'confirmed' if txdata['confirmations'] > 0
            else 'unconfirmed',
            'raw': txdata
        }

    def _get_value_sum(self, addrs, txs):
        my_addrs = list(set(addrs) & set(self._tokens))
        value = 0
        for tx in txs:
            if tx['addresses'][0] in my_addrs:
                value += float(tx['value'])
        return value

class Btc1TrezorAPI(TrezorAPI):
    base_url = 'https://btc1.trezor.io'
    symbol = 'BTC'


class Btc2TrezorAPI(TrezorAPI):
    base_url = 'https://btc2.trezor.io'
    symbol = 'BTC'


class Ltc1TrezorAPI(TrezorAPI):
    base_url = 'https://ltc1.trezor.io'
    symbol = 'LTC'
