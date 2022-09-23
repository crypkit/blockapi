from blockapi.services import BlockchainAPI


class DigonchainAPI(BlockchainAPI):
    """
    coins: vechain
    API docs: https://vethor-pubnode.digonchain.com/doc/swagger-ui/
    Explorer: https://explorer.vtho.net/
    """

    active = True

    symbol = 'VET'
    # the docs say this node may not be reliable enough
    # but seems there's no other
    # TODO: find a better one in the future
    base_url = 'https://vethor-pubnode.digonchain.com'
    rate_limit = 0
    coef = 1e-18
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': '/accounts/{address}',
    }

    def get_balance(self):
        response = self.request('get_balance', address=self.address)
        if not response:
            return None
        else:
            try:
                balance = response['balance']
                balance = int(balance, 16)
                retval = balance * self.coef
            except (KeyError, ValueError):
                return None

        return [{'symbol': self.symbol, 'amount': retval}]
