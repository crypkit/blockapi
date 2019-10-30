from blockapi.services import (
    BlockchainAPI
)


class ChainSoAPI(BlockchainAPI):
    """
    Multi coins: bitcoin, litecoin, dogecoin, zcash, dash
    Does't support xpub/ypub/zpub :(
    API docs: https://chain.so/api
    Explorer: 
    """

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
            address=self.address,
            with_cloudflare=True
        )
        if response['status'] == 'fail':
            return None
        return response['data']


class ChainSoBitcoinAPI(ChainSoAPI):
    active = False
    symbol = 'BTC'
    coef = 1e-8


class ChainSoLitecoinAPI(ChainSoAPI):
    active = False
    symbol = 'LTC'
    coef = 1e-8


class ChainSoDogecoinAPI(ChainSoAPI):
    symbol = 'DOGE'
    coef = 1


class ChainSoZcashAPI(ChainSoAPI):
    symbol = 'ZEC'
    coef = 1


class ChainSoDashAPI(ChainSoAPI):
    symbol = 'DASH'
    coef = 1
