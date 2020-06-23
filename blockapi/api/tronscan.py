from decimal import Decimal
from blockapi.services import (
    BlockchainAPI,
    on_failure_return_none
)


class TronscanAPI(BlockchainAPI):
    """
    coins: tron
    API docs: https://github.com/tronscan/tronscan-frontend/blob/dev2019/document/api.md
    Explorer: https://tronscan.org
    """

    active = True

    symbol = 'TRX'
    base_url = 'https://apilist.tronscan.org/api'
    rate_limit = 0
    coef = "1e-6"
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': '/account?address={address}',
        'get_trc10_tokenlist': '/token?limit=10000',
    }

    @on_failure_return_none()
    def get_balance(self):
        response = self.request('get_balance',
                                address=self.address)
        if not response:
            return None

        token_map = {}

        trc10_tokenlist = self.request('get_trc10_tokenlist')['data']
        for token in trc10_tokenlist:
            token_map[token['tokenID']] = {'abbr': token['abbr'], 'precision': token['precision']}

        balances = []
        for coin in response['tokenBalances']:
            if coin['name'] == '_':
                symbol = self.symbol
                owner_address = self.address
                coin_coef = "1e-6"
            else:
                token = token_map.get(int(coin['name']))
                # Test address has token with 1002001 which doesn't return in 10000 tokens in token list.
                # So we simply ignore this
                if token is None:
                    continue
                symbol = token.get('abbr', '')
                owner_address = coin['owner_address']

                coin_coef = "1e-{}".format(token.get('precision', 1))

            balances.append({'symbol': symbol,
                             'amount': Decimal(coin['balance']) * Decimal(coin_coef),
                             'address': owner_address})
        for coin in response['trc20token_balances']:
            balances.append({'symbol': coin['symbol'], 
                             'amount': Decimal(coin['balance']) * Decimal("1e-{}".format(coin['decimals'])),
                             'address': None})

        return balances
