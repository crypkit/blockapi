from blockapi.services import (
    BlockchainAPI
)

class BinanceAPI(BlockchainAPI):
    """
    coins: binance coin
    API docs: https://docs.binance.org/api-reference/dex-api/paths.html
    Explorer: 
    """

    active = True

    currency_id = 'binance-coin'
    base_url = 'https://dex.binance.org/api/v1'
    rate_limit = 0
    coef = 1
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': '/account/{address}',
    }

    def get_balance(self):
        response = self.request('get_balance',
                                address=self.address)
        if not response:
            return 0

        try:
            return [{
                'symbol': bal['symbol'],
                'amount': float(bal['free']) * self.coef
            } for bal in response['balances']]
        except ValueError:
            return 0
