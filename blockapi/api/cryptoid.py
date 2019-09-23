from blockapi.services import (
    BlockchainAPI
)


class CryptoIDAPI(BlockchainAPI):
    """
    Multi coins
    API docs: https://chainz.cryptoid.info/api.dws
    Explorer: https://chainz.cryptoid.info
    """

    active = True

    currency_id = None
    base_url = 'http://chainz.cryptoid.info'
    rate_limit = 0
    coef = 1e-8
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': '/{currency_id}/api.dws?q=getbalance&a={address}&key={api_key}',
    }

    def get_balance(self):
        response = self.request('get_balance',
                                api_key=self.api_key,
                                currency_id=self.currency_id,
                                address=self.address)

        return response * self.coef

class CryptoIDLitecoinAPI(CryptoIDAPI):

    currency_id = 'ltc'

class CryptoIDDashAPI(CryptoIDAPI):

    currency_id = 'dash'
    coef = 1

class CryptoIDGroestlcoinAPI(CryptoIDAPI):

    currency_id = 'grs'
    coef = 1
