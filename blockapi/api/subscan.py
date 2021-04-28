from abc import ABC
from decimal import Decimal

from blockapi.services import BlockchainAPI, AddressNotExist, APIError


class SubscanAPI(BlockchainAPI, ABC):
    """
    API docs: https://docs.api.subscan.io/
    Explorer: https://www.subscan.io
    """

    api_url = 'api.subscan.io'
    rate_limit = 0
    coef = 1
    max_items_per_page = 50
    page_offset_step = 1
    confirmed_num = None
    xpub_support = True

    supported_requests = {
        'get_balance': '/api/v2/scan/search',
        'get_txs': '/api/scan/extrinsics',
        'get_rewards': '/api/scan/account/reward_slash',
        'get_stacking': '/api/scan/staking_history'
    }

    def __init__(self, address, *args, **kwargs):
        super().__init__(address)
        self._headers = {
            'Content-Type': 'application/json'
        }

    def get_balance(self):
        body = '{"key": "' + self.address + '", "row": "1", "page": "0"}'

        response = self.request(
            'get_balance',
            body=body,
            with_cloudflare=True,
            headers=self._headers
        )

        if response['code'] == 0:
            return [{
                'symbol': self.symbol,
                'amount': Decimal(response['data']['account']['balance']) * self.coef
            }]
        elif response['code'] == 10004:
            raise AddressNotExist()
        else:
            raise APIError(response['message'])

    def get_txs(self, offset=0, limit=20, unconfirmed=False):
        body = '{ "key": "' + self.address + '", "signed": "all", ' \
                ' "row": ' + ('1,' if (limit is None) else str(limit) + ', ') + \
                ' "page": ' + ('0' if (offset is None) else str(offset)) + '}'

        response = self.request(
            'get_txs',
            body=body,
            with_cloudflare=True,
            headers=self._headers
        )

        if response['code'] == 0:
            return [self._parse_tx(t) for t in response['data']['extrinsics']]
            # TODO if unconfirmed
        elif response['code'] == 10004:
            raise AddressNotExist()
        else:
            raise APIError(response['message'])

    def _parse_tx(self, tx):
        # TODO map TX
        return {
        }

    def get_rewards(self, offset=0, limit=20):
        body = '{"address": "' + self.address + '", "row": 20, "page": 0}'

        response = self.request(
            'get_rewards',
            body=body,
            with_cloudflare=True,
            headers=self._headers
        )

        if response['code'] == 0:
            return response['data']['list'] if response['data']['list'] is not None else []
        else:
            raise APIError(response['message'])

    def get_staking(self, offset=0, limit=20):
        # TODO
        pass


class SubscanPolkaAPI(SubscanAPI):
    chain_name = 'polkadot'
    symbol = 'DOT'
    base_url = 'https://' + chain_name + '.' + SubscanAPI.api_url


class SubscanKusamaAPI(SubscanAPI):
    chain_name = 'kusama'
    symbol = 'KSM'
    base_url = 'https://' + chain_name + '.' + SubscanAPI.api_url
