from pytest import mark

from blockapi.api import OntioAPI
from blockapi.test_data import test_addresses


class TestOntioAPI:
    ADDRESS = test_addresses['ONT'][0]

    @mark.vcr()
    def test_get_balance(self):
        api = OntioAPI(self.ADDRESS)
        result = api.get_balance()
