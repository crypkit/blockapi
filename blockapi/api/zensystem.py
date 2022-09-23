from blockapi.services import BlockchainAPI


class ZensystemAPI(BlockchainAPI):
    """
    coins: horizen
    API docs: ?
    Explorer: https://explorer.zensystem.io/
    """

    active = True

    symbol = 'ZEN'
    base_url = 'https://explorer.zensystem.io/api'
    rate_limit = 0
    coef = 1
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': '/addr/{address}',
    }

    def get_balance(self):
        response = self.request('get_balance', address=self.address)
        if not response:
            return None

        retval = response.get('balance') * self.coef
        return [{'symbol': self.symbol, 'amount': retval}]
