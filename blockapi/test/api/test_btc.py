from pytest import mark

from blockapi.api.btc import BtcAPI
from blockapi.test_data import test_addresses


class TestBtcAPI:
    ADDRESS = test_addresses['BCH'][0]

    @mark.vcr()
    def test_get_balance(self):
        api = BtcAPI(address=self.ADDRESS)
        result = api.get_balance()

        assert result == [{'symbol': 'BCH', 'amount': 505295.97471374}]
