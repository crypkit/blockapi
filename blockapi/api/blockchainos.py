import dateutil.parser

from blockapi.services import BlockchainAPI


class BlockchainosAPI(BlockchainAPI):
    """
    coins: boscoin
    API docs: http://devteam.blockchainos.org/docs/api/
    Explorer: https://explorer.boscoin.io/
    """

    active = True

    symbol = 'BOS'
    base_url = 'https://mainnet.blockchainos.org'
    rate_limit = 0
    coef = 1e-7
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': '/api/v1/accounts/{address}',
        'get_txs': '/api/v1/accounts/{address}'
        '/transactions?limit={limit}&reverse=true',
    }

    def get_balance(self):
        response = self.request('get_balance', address=self.address)
        if not response:
            return None

        try:
            balance = int(response.get('balance'))
        except (KeyError, ValueError):
            return None

        return [{'symbol': self.symbol, 'amount': balance * self.coef}]

    def get_txs(self, offset=None, limit=100, unconfirmed=False):
        if 'get_txs_next' not in self.supported_requests:
            response = self.request('get_txs', address=self.address, limit=limit)
            self.supported_requests['get_txs_next'] = response['_links']['prev']['href']

        else:
            response = self.request('get_txs_next')
            self.supported_requests['get_txs_next'] = response['_links']['prev']['href']

        return [self.parse_tx(tx) for tx in response['_embedded']['records']]

    def parse_tx(self, tx):
        operations = []

        operation_url = tx['_links']['operations']['href']
        self.supported_requests['get_operations'] = operation_url.replace(
            '{?cursor,limit,order}', ''
        )
        response = self.request('get_operations')

        for operation in response['_embedded']['records']:
            op_from_address = operation['source']
            op_to_address = operation['target']
            op_hash = operation['tx_hash']
            op_amount = operation['body']['amount']
            op_type = operation['type']
            op_confirmed = dateutil.parser.parse(operation['confirmed'])
            operations.append(
                {
                    'from_address': op_from_address,
                    'to_address': op_to_address,
                    'hash': op_hash,
                    'amount': float(op_amount) * self.coef,
                    'type': op_type,
                    'direction': (
                        'outgoing' if op_from_address == self.address else 'incoming'
                    ),
                    'confirmed': op_confirmed,
                    'raw': operation,
                }
            )

        return {
            'date': dateutil.parser.parse(tx['created']),
            'fee': float(tx['fee']) * self.coef,
            'hash': tx['hash'],
            'is_error': False,
            'kind': 'transaction',
            'status': 'confirmed',
            'operations': operations,
            'raw': tx,
        }
