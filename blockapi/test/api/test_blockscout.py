from pytest import mark

from blockapi.api import BlockscoutEthereumClassicAPI, BlockscoutXdaiAPI
from blockapi.test_data import test_addresses


class TestBlockscoutXdaiAPI:
    ADDRESS = test_addresses['STAKE'][0]

    @mark.vcr()
    def test_get_balance(self):
        api = BlockscoutXdaiAPI(self.ADDRESS)
        result = api.get_balance()

        assert len(result) == 4


class TestBlockscoutEthereumClassicAPI:
    ADDRESS = test_addresses['ETC'][0]

    @mark.vcr()
    def test_get_balance(self):
        api = BlockscoutEthereumClassicAPI(self.ADDRESS)
        result = api.get_balance()

        assert len(result) == 3
