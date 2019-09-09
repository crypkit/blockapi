from blockapi.services import (
    BlockchainAPI,
    set_default_args_values,
    APIError,
    AddressNotExist,
    BadGateway,
    GatewayTimeOut,
    InternalServerError
    )
import coinaddr

class ChainSoAPI(BlockchainAPI):
    """
    Multi coins: bitcoin, litecoin, dogecoin, zcash, dash
    Does't support xpub/ypub/zpub :(
    API docs: https://chain.so/api
    Explorer: 
    """

    active = False

    currency_id = None
    symbol = None
    base_url = 'https://chain.so/api/v2'
    rate_limit = 0.2  # 5 per second
    coef = None
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': '/get_address_balance/{symbol}/{address}',
        'get_txs': '/address/{symbol}/{address}'
    }

    def __init__(self, address, api_key=None):
        super().__init__(address, api_key)

    def get_balance(self):
        response = self._request('get_balance')
        if not response:
            return 0

        return float(response['confirmed_balance']) * self.coef

    # don't set default args, we can get all transactions at once
    # @set_default_args_values
    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        response = self._request('get_txs')
        if not response:
            return []

        txs = response['txs']
        # filter records manually because from api we get all txs
        if offset or limit:
            txs = txs[offset:limit]

        return [self.parse_tx(t) for t in txs]

    def parse_tx(self, tx):
        return tx

    def _request(self, method):
        response = self.request(
            method,
            symbol=self.symbol,
            address=self.address
        )
        if response['status'] == 'fail':
            return None
        return response['data']


class ChainSoBitcoinAPI(ChainSoAPI):
    currency_id = 'bitcoin'
    symbol = 'BTC'
    coef = 1e-8

    def __init__(self,address,api_key=None):
        if coinaddr.validate('btc',address).valid:
            super().__init__(address,api_key)
        else:
            raise ValueError('Not a valid bitcoin address.')
