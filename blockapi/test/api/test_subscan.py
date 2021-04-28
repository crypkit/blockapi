from decimal import Decimal

from pytest import mark

from blockapi.api.subscan import SubscanPolkaAPI
from blockapi.test_data import test_addresses


class TestSubscanAPI:
    ADDRESS = test_addresses['DOT'][0]

    # @mark.vcr()
    def test_get_balance(self):
        api = SubscanPolkaAPI(address=self.ADDRESS)
        result = api.get_balance()

        assert result == [{'symbol': 'DOT', 'amount': Decimal('1000.6244112896')}]

    # @mark.vcr()
    def test_get_txs(self):
        api = SubscanPolkaAPI(address=self.ADDRESS)
        result = api.get_txs()

        assert isinstance(result, list)
        assert len(result) == 20

    # @mark.vcr()
    def test_rewards(self):
        api = SubscanPolkaAPI(address=self.ADDRESS)
        result = api.get_rewards()

        assert isinstance(result, list)
        assert len(result) == 2

    # @mark.vcr()
    def test_staking(self):
        # TODO
        pass
