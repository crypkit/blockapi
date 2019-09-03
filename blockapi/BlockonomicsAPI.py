from .services import BlockchainAPI,set_default_args_values,APIError,AddressNotExist,BadGateway,GatewayTimeOut

class BlockonomicsAPI(BlockchainAPI):
    """
    Bitcoin
    API docs: https://www.blockonomics.co/views/api.html
    Explorer: https://www.blockonomics.co
    """

    active = True

    currency_id = 'bitcoin'
    base_url = 'https://www.blockonomics.co/api'
    # rate_limit = 30
    coef = 1e-8
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': '/balance'
    }

    # def process_error_response(self, response):
    #     if response.text == 'Invalid Bitcoin Address':
    #         raise AddressNotExist()
    #     # else
    #     super().process_error_response(response)

    def get_balance(self):
        body = '{"addr": "' + self.address + '"}'
        response = self.request('get_balance', body=body)
        if not response.get('response'):
            return 0

        balance = sum(r['confirmed'] * self.coef for r in response['response'])
        return balance

