from blockapi.services import BlockchainAPI


class TzStatsAPI(BlockchainAPI):
    """
    Tezos
    Explorer: https://api.tzstats.com/explorer/
    Docs: https://tzstats.com/docs/api/index.html
    """

    symbol = 'XTZ'
    base_url = 'https://api.tzstats.com/'
    rate_limit = 0
    coef = 1
    max_items_per_page = 50
    page_offset_step = 1

    supported_requests = {'get_account': 'explorer/account/{address}'}

    def get_balance(self):
        balance = self.request('get_account', address=self.address)
        return [{'symbol': self.symbol, 'amount': float(balance['spendable_balance'])}]

    def get_account(self):
        response = self.request('get_account', address=self.address)

        response['manager'] = self.request('get_account', address=response['manager'])
        response['delegate'] = self.request('get_account', address=response['delegate'])
        return response
