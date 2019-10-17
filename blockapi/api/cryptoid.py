from blockapi.services import (
    BlockchainAPI,APIKeyMissing
)


class CryptoIDAPI(BlockchainAPI):
    """
    Multi coins
    API docs: https://chainz.cryptoid.info/api.dws
    Explorer: https://chainz.cryptoid.info
    """

    active = True

    symbol = None
    base_url = 'http://chainz.cryptoid.info'
    rate_limit = 0
    coef = 1e-8
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': '/{symbol}/api.dws?q=getbalance&a={address}&key={api_key}',
    }

    def __init__(self, address, api_key=None):
        if api_key is None:
            raise APIKeyMissing

        super().__init__(address, api_key)


    def get_balance(self):
        response = self.request('get_balance',
                                api_key=self.api_key,
                                symbol=self.symbol.lower(),
                                address=self.address)

        return response * self.coef


class CryptoIDLitecoinAPI(CryptoIDAPI):
    symbol = 'LTC'


class CryptoIDDashAPI(CryptoIDAPI):
    symbol = 'DASH'
    coef = 1


class CryptoIDGroestlcoinAPI(CryptoIDAPI):
    symbol = 'GRS'
    coef = 1
