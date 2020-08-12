from pytest import mark

from blockapi.api import AmberdataAPI
from blockapi.test_init import test_addresses


class TestAmberdataAPI:
    ADDRESS = test_addresses['ETH'][0]
    API_KEY = 'enter valid key if you want to re-fetch vcr'

    @mark.vcr(filter_headers=['x-api-key'])
    def test_get_balance(self):
        api = AmberdataAPI(self.ADDRESS, self.API_KEY)
        result = api.get_balance()

        assert len(result) == 10
        eth_bal = next(b for b in result if b['symbol'] == 'ETH')
        assert eth_bal['amount'] == 0.0

    @mark.vcr(filter_headers=['x-api-key'])
    def test_get_token_info(self):
        result = AmberdataAPI.get_token_info(
            token_address='0xdac17f958d2ee523a2206206994597c13d831ec7',
            api_key=self.API_KEY
        )

        assert result['symbol'] == 'USDT'
