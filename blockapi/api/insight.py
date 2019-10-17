from blockapi.services import (
    BlockchainAPI
)


class InsightAPI(BlockchainAPI):
    """
    coins: zcash, ravencoin, bitcoin
    """

    active = True

    rate_limit = 0
    coef = 1e-8
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': '/addr/{address}/balance',
    }

    def get_balance(self):
        response = self.request('get_balance',
                                address=self.address)
        if not response:
            return 0

        return response * self.coef


class BitpayAPI(InsightAPI):
    """
    coins: bitcoin
    API docs: 
    Explorer: 
    """
    symbol = 'BTC'
    base_url = 'https://insight.bitpay.com/api'


class MercerweissAPI(InsightAPI):
    """
    coins: zcash
    API docs: http://insight.mercerweiss.com/api
    Explorer: http://insight.mercerweiss.com/
    """
    symbol = 'ZEC'
    base_url = 'http://insight.mercerweiss.com/api'


class RavencoinAPI(InsightAPI):
    """
    coins: ravencoin
    API docs: https://github.com/RavenDevKit/insight-api
    Explorer: https://ravencoin.network
    """
    symbol = 'RVN'
    base_url = 'https://ravencoin.network/api'


class InsightLitecoreAPI(InsightAPI):
    """
    coins: litecoin
    API docs: 
    Explorer: https://insight.litecore.io
    """
    active = False
    symbol = 'LTC'
    base_url = 'https://insight.litecore.io/api'
