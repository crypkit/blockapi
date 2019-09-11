from blockapi.services import (
    BlockchainAPI,
    set_default_args_values,
    APIError,
    AddressNotExist,
    BadGateway,
    GatewayTimeOut,
    InternalServerError
    )
import coinaddr
import pytz
from datetime import datetime

class ZchainAPI(BlockchainAPI):
    """
    coins: zcash
    API docs: https://explorer.zcha.in/api
    Explorer: https://explorer.zcha.in/
    """

    active = True

    currency_id = 'zcash'
    base_url = 'https://api.zcha.in'
    rate_limit = 0
    coef = 1
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': '/v2/mainnet/accounts/{address}',
    }

    def __init__(self, address, api_key=None):
        if coinaddr.validate('zec', address).valid:
            super().__init__(address,api_key)
        else:
            raise ValueError('Not a valid zcash address: {}'.format(address))

    def get_balance(self):
        response = self.request('get_balance',
                                address=self.address)
        if not response:
            return 0

        return response.get('balance') * self.coef

