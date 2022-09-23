from blockapi.services import BlockchainAPI


class EthplorerAPI(BlockchainAPI):
    """
    Ethereum
    API docs: https://github.com/EverexIO/Ethplorer/wiki/Ethplorer-API
    Explorer: https://ethplorer.io
    """

    symbol = 'ETH'
    base_url = 'http://api.ethplorer.io'
    default_api_key = 'freekey'
    rate_limit = 0.2
    coef = 1e-18
    start_offset = None
    max_items_per_page = None
    page_offset_step = None

    supported_requests = {'get_info': '/getAddressInfo/{address}?apiKey={api_key}'}

    def __init__(self, address, api_key=None):
        if not api_key:
            api_key = self.default_api_key

        super().__init__(address, api_key)

        # cache info
        self._info = None

        if self.api_key != self.default_api_key:
            self.rate_limit = 0.1

    def get_balance(self):
        balances = []
        response = self.info

        if response.get('ETH', {}).get('balance'):
            balances.append(
                {'symbol': self.symbol, 'amount': response['ETH']['balance']}
            )

        for token in response.get('tokens', []):
            info = token['tokenInfo']
            decimals = int(info['decimals']) if info.get('decimals') else 18

            balances.append(
                {
                    'symbol': info.get('symbol', 'unknown'),
                    'address': info['address'],
                    'amount': token['balance'] * pow(10, -decimals),
                    'name': info.get('name', 'Unknown'),
                }
            )

        if not balances:
            return None

        return balances

    @property
    def info(self):
        if not self._info:
            self._info = self.request(
                'get_info', address=self.address, api_key=self.api_key
            )
        return self._info
