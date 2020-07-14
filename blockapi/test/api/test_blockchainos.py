from pytest import mark

from blockapi.api.blockchainos import BlockchainosAPI
from blockapi.test_init import test_addresses


class TestBlockchainosAPI:
    ADDRESS = test_addresses['BOS'][0]

    @mark.vcr()
    def test_get_balance(self):
        api = BlockchainosAPI(address=self.ADDRESS)
        result = api.get_balance()

        assert result == [{'symbol': 'BOS', 'amount': 454146425.404}]

    @mark.vcr()
    def test_get_txs(self):
        api = BlockchainosAPI(address=self.ADDRESS)
        result = api.get_txs(limit=10)

        assert isinstance(result, list)
        assert len(result) == 10
