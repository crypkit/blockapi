from datetime import datetime

import pytz

from blockapi.services import AddressNotExist, APIError, BlockchainAPI


class CardanoExplorerAPI(BlockchainAPI):
    """
    Cardano
    API docs: https://cardanodocs.com/technical/explorer/api/
    Explorer: https://cardanoexplorer.com
    """

    symbol = 'ADA'
    base_url = 'https://cardanoexplorer.com/api'
    rate_limit = 0
    coef = 1e-6

    supported_requests = {'get_summary': '/addresses/summary/{address}'}

    def get_balance(self):
        summary = self._get_summary()
        retval = int(summary['Right']['caBalance']['getCoin']) * self.coef
        return [{'symbol': self.symbol, 'amount': retval}]

    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        summary = self._get_summary()
        txs = summary['Right']['caTxList']
        return [self.parse_tx(t) for t in txs]

    def parse_tx(self, tx):
        my_input = next(
            (i for i in tx['ctbInputs'] if i[0].lower() == self.address.lower()), None
        )

        my_output = next(
            (i for i in tx['ctbOutputs'] if i[0].lower() == self.address.lower()), None
        )

        fee = None

        if my_input:
            fee = int(tx['ctbInputSum']['getCoin']) - int(tx['ctbOutputSum']['getCoin'])

            to_address = tx['ctbInputs'][0][0] if len(tx['ctbInputs']) else None
            from_address = self.address
            amount = int(my_input[1]['getCoin']) * self.coef

        else:
            from_address = tx['ctbOutputs'][0][0] if len(tx['ctbOutputs']) else None
            to_address = self.address
            amount = int(my_output[1]['getCoin']) * self.coef

        return {
            'date': datetime.fromtimestamp(tx['ctbTimeIssued'], pytz.utc),
            'from_address': from_address,
            'to_address': to_address,
            'amount': amount,
            'fee': fee,
            'gas': {},
            'hash': tx['ctbId'],
            'confirmed': None,
            'is_error': False,
            'type': 'normal',
            'kind': 'transaction',
            'direction': 'outgoing' if my_input else 'incoming',
            'raw': tx,
        }

    def _get_summary(self):
        summary = self.request('get_summary', address=self.address)
        if summary.get('Left'):
            self._process_error(summary['Left'])
            return None

        return summary

    @staticmethod
    def _process_error(msg):
        if msg == 'Invalid Cardano address!':
            raise AddressNotExist()
        else:
            raise APIError(msg)
