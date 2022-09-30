from os import environ

from pytest import mark

from blockapi.api import AmberdataAPI
from blockapi.test_data import test_addresses


class TestAmberdataAPI:
    ADDRESS = test_addresses['ETH'][0]
    API_KEY = environ.get('AMBERDATAAPI_KEY', 'None')

    @mark.vcr(filter_headers=['x-api-key'])
    def test_get_balance(self):
        api = AmberdataAPI(self.ADDRESS, self.API_KEY)
        result = api.get_balance()

        assert len(result) == 57
        eth_bal = next(b for b in result if b['symbol'] == 'ETH')
        assert eth_bal['amount'] == 325000.4290170703

    @mark.vcr(filter_headers=['x-api-key'])
    def test_get_token_info(self):
        result = AmberdataAPI.get_token_info(
            token_address='0xdac17f958d2ee523a2206206994597c13d831ec7',
            api_key=self.API_KEY,
        )

        assert result['symbol'] == 'USDT'
