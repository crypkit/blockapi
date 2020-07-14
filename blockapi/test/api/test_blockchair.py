from pytest import mark

from blockapi.api.blockchair import (BlockchairGroestlcoinAPI,
                                     BlockchairBitcoinSvAPI)
from blockapi.test_init import test_addresses


class TestBlockchairAPI:
    GROESTL_ADDRESS = test_addresses['GRS'][0]
    BSV_ADDRESS = test_addresses['BSV'][0]

    @mark.vcr()
    def test_get_balance_groestl_coin(self):
        api = BlockchairGroestlcoinAPI(address=self.GROESTL_ADDRESS)
        result = api.get_balance()

        assert result == [{'symbol': 'GRS', 'amount': 330.00184162}]

    @mark.vcr()
    def test_get_balance_bitcoin_sv(self):
        api = BlockchairBitcoinSvAPI(address=self.BSV_ADDRESS)
        result = api.get_balance()

        assert result == [{'symbol': 'BSV', 'amount': 0.39608498000000003}]
