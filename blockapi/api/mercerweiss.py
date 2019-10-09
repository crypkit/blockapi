from blockapi.services import (
    BlockchainAPI
)


class MercerweissAPI(BlockchainAPI):
    """
    coins: zcash
    API docs: http://insight.mercerweiss.com/api
    Explorer: http://insight.mercerweiss.com/
    """

    active = True

    symbol = 'ZEC'
    base_url = 'http://insight.mercerweiss.com/api'
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
