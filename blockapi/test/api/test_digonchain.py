from pytest import mark

from blockapi.api.digonchain import DigonchainAPI
from blockapi.test_data import test_addresses


class TestDigonchainAPI:
    ADDRESS = test_addresses['VET'][0]

    @mark.vcr()
    def test_get_balance(self):
        api = DigonchainAPI(address=self.ADDRESS)
        result = api.get_balance()

        assert result == [{'symbol': 'VET', 'amount': 1099261.20775139}]
