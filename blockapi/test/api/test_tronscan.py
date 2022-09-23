from pytest import mark

from blockapi.api.tronscan import TronscanAPI
from blockapi.test_data import test_addresses


class TestTronscanAPI:
    ADDRESS = test_addresses['TRX'][0]

    @mark.vcr()
    def test_get_balance(self):
        api = TronscanAPI(address=self.ADDRESS)
        result = api.get_balance()

        assert next((r["amount"] for r in result if r["symbol"] == "TRX")) == 0.588285
        assert len(result) == 55
