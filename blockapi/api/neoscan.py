from datetime import datetime

import pytz

from blockapi.services import APIError, BlockchainAPI


class NeoscanAPI(BlockchainAPI):
    """
    coins: neocoin
    API docs: https://neoscan.io/docs/index.html#api-v1
    Explorer:
    """

    active = True

    symbol = 'NEO'
    base_url = 'https://api.neoscan.io/api/main_net/v1'
    rate_limit = 0
    coef = 1
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': '/get_balance/{address}',
        'get_txs': '/get_address_abstracts/{address}/{page}',
    }

    def __init__(self, address, api_key=None):
        super().__init__(address, api_key)
        paging_params = self.get_tx_paging_params()
        if paging_params is None:
            raise APIError('Can\'t initialize API paging.')
        else:
            self.max_items_per_page = self.page_offset_step = paging_params[1]
            self.total_txs_count = paging_params[2]

    def get_balance(self):
        response = self.request('get_balance', address=self.address)
        if not response:
            return None

        for bal in response['balance']:
            if bal.get('asset_symbol') == self.symbol:
                return [
                    {'symbol': self.symbol, 'amount': bal.get('amount') * self.coef}
                ]

        return None

    def get_tx_paging_params(self):
        # total pages can be found on the first page
        response = self.request('get_txs', address=self.address, page=1)
        if 'total_pages' in response and 'page_size' in response:
            return (
                int(response['total_pages']),
                int(response['page_size']),
                int(response['total_entries']),
            )
        else:
            return None

    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        page = (offset // self.max_items_per_page) + 1
        # page_offset 'should be set' offset % self.max_items_per_page

        if limit > self.total_txs_count - offset:
            limit = self.total_txs_count - offset

        result = []

        while True:
            response = self.request('get_txs', address=self.address, page=page)

            if 'entries' in response:
                for t in response['entries']:
                    result.append(self.parse_tx(t))
                    limit -= 1
                    if limit == 0:
                        return result
            else:
                return result

            page += 1

    def parse_tx(self, tx):
        if tx['address_from'] == self.address:
            direction = 'outgoing'
        else:
            direction = 'incoming'

        return {
            'date': datetime.fromtimestamp(tx['time'], pytz.utc),
            'from_address': tx['address_from'],
            'to_address': tx['address_to'],
            'amount': tx['amount'],
            'fee': None,
            'hash': tx['txid'],
            'confirmed': None,
            'is_error': False,
            'type': 'normal',
            'kind': 'transaction',
            'direction': direction,
            'status': 'confirmed',
            'raw': tx,
        }
