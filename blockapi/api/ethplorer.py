from blockapi.services import (
    BlockchainAPI
)


class EthplorerAPI(BlockchainAPI):
    """
    Ethereum
    API docs: https://github.com/EverexIO/Ethplorer/wiki/Ethplorer-API
    Explorer: https://ethplorer.io
    """

    currency_id = 'ethereum'
    base_url = 'http://api.ethplorer.io'
    default_api_key = 'freekey'
    rate_limit = 0
    coef = 1e-18
    start_offset = None
    max_items_per_page = None
    page_offset_step = None

    supported_requests = {
        'get_info': '/getTokenInfo/{address}?apiKey={api_key}'
    }

    def __init__(self, address, api_key=None):
        if not api_key:
            api_key = self.default_api_key
        super().__init__(address, api_key)

    def get_balance(self):
        balances = []
        response = self.get_info()

        balances.append({
            'symbol': 'ETH',
            'amount': response['ETH']['balance']
        })

        for token in response.get('tokens', []):
            info = token['tokenInfo']
            balances.append({
                'symbol': info['symbol'],
                'address': info['address'],
                'amount': token['balance'] * pow(10, -int(info['decimals'])),
                'name': info['name']
            })

        return balances

    def get_info(self):
        return self.request(
            'get_info',
            address=self.address,
            api_key=self.api_key
        )
