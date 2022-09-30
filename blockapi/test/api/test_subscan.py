from decimal import Decimal

from pytest import mark

from blockapi.api.subscan import SubscanPolkaAPI, SubscanWestendAPI
from blockapi.test_data import test_addresses


class TestSubscanAPI:
    ADDRESS = test_addresses['WND'][0]

    @mark.vcr()
    def test_get_balance(self):
        api = SubscanWestendAPI(address=self.ADDRESS)
        result = api.get_balance()

        assert result == [{'symbol': 'WND', 'amount': Decimal('1.140399983849')}]

    @mark.vcr()
    def test_get_txs(self):
        api = SubscanWestendAPI(address=self.ADDRESS)
        result = api.get_txs()

        assert isinstance(result, list)
        assert len(result) == 3

    @mark.vcr()
    def test_rewards(self):
        api = SubscanWestendAPI(address=self.ADDRESS)
        result = api.get_rewards()

        assert isinstance(result, list)
        assert result[0]['amount'] == Decimal('4.967762520373')

    @mark.vcr()
    def test_staking(self):
        api = SubscanWestendAPI(address=self.ADDRESS)
        result = api.get_staking()

        assert isinstance(result, Decimal)
        assert result == Decimal('0.98039999247')
