from pytest import mark

from blockapi.api.digonchain import DigonchainAPI
from blockapi.test_init import test_addresses


class TestDigonchainAPI:
    ADDRESS = test_addresses['VET'][0]

    @mark.vcr()
    def test_get_balance(self):
        api = DigonchainAPI(address=self.ADDRESS)
        result = api.get_balance()

        assert result == [{'symbol': 'VET', 'amount': 553093.54494999}]
