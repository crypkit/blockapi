from blockapi.services import BlockchainAPI


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
        response = self.request('get_balance', address=self.address)
        if not response:
            return []

        return [{'symbol': self.symbol, 'amount': response * self.coef}]


class BitpayAPI(InsightAPI):
    """
    coins: bitcoin
    API docs:
    Explorer:
    """

    active = False  # no longer available
    symbol = 'BTC'
    base_url = 'https://insight.bitpay.com/api'


class MercerweissAPI(InsightAPI):
    """
    coins: zcash
    API docs: http://insight.mercerweiss.com/api
    Explorer: http://insight.mercerweiss.com/
    """

    active = False  # no longer available
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


class InsightDcrdataAPI(InsightAPI):
    """
    coins: decred
    API docs: https://github.com/decred/dcrdata/blob/master/api/Insight_API_documentation.md
    Explorer: https://explorer.dcrdata.org
    """

    symbol = 'DCR'
    base_url = 'https://explorer.dcrdata.org/insight/api'
