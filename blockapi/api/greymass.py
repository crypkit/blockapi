from blockapi.services import BlockchainAPI


class GreymassAPI(BlockchainAPI):
    """
    coins: eos
    API docs: https://github.com/greymass/eosio-api-ext/wiki
    /API-Request-Response-Examples
    Explorer:
    """

    active = True

    symbol = 'EOS'
    base_url = 'https://eos.greymass.com/v1'
    rate_limit = 0
    coef = 1
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': '/chain/get_currency_balances',
    }

    def get_balance(self):
        body = '{"account": "' + self.address + '"}'
        response = self.request('get_balance', body=body)
        if not response:
            return None

        # {‘symbol’: _, ‘address’: _, ‘price’: _, ‘name’: ?} ]

        try:
            return [
                {
                    "symbol": item["symbol"],
                    "address": item["code"],
                    "amount": float(item["amount"]),
                    "name": None,
                }
                for item in response
            ]
        except KeyError:
            return None
