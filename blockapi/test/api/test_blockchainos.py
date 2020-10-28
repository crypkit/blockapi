from pytest import mark

from blockapi.api.blockchainos import BlockchainosAPI
from blockapi.test_data import test_addresses


class TestBlockchainosAPI:
    ADDRESS = test_addresses['BOS'][0]

    @mark.vcr()
    def test_get_balance(self):
        api = BlockchainosAPI(address=self.ADDRESS)
        result = api.get_balance()

        assert result == [{'symbol': 'BOS', 'amount': 545879431.776}]

    @mark.vcr()
    def test_get_txs(self):
        api = BlockchainosAPI(address=self.ADDRESS)
        result = api.get_txs(limit=10)

        assert isinstance(result, list)
        assert len(result) == 10
