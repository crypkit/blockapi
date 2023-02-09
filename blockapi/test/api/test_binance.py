from pytest import mark

from blockapi.api.binance import BinanceAPI
from blockapi.test_data import test_addresses


class TestBinanceAPI:
    ADDRESS = test_addresses["BNB"][0]

    def test_init(self):
        api = BinanceAPI(address=self.ADDRESS)
        assert api

    @mark.vcr()
    def test_get_balance(self):
        api = BinanceAPI(address=self.ADDRESS)
        result = api.get_balance()

        assert isinstance(result, list)
        assert len(result) == 103

    @mark.vcr()
    def test_get_txs(self):
        api = BinanceAPI(address=self.ADDRESS)
        result = api.get_txs()

        assert isinstance(result, list)
        assert len(result) == 100
