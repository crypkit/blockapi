from blockapi.services import (
    BlockchainAPI,
    on_failure_return_none
)


class BlockscoutAPI(BlockchainAPI):
    """
    coins: etc
    API docs: https://blockscout.com/etc/mainnet/api_docs
    Explorer: https://blockscout.com
    """

    active = True

    symbol = 'ETC'
    base_url = 'https://blockscout.com/etc/mainnet/api?'
    rate_limit = 0
    coef = 1e-18
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': 'module=account&action=eth_get_balance&address={address}',
    }

    @on_failure_return_none()
    def get_balance(self):
        response = self.request('get_balance',
                                address=self.address)
        if not response:
            return None

        retval = int(response['result'], 16) * self.coef
        return [{'symbol': self.symbol, 'amount': retval}]
