from pytest import mark

from blockapi.api.tzscan import TzscanAPI
from blockapi.test_data import test_addresses


class TestTzscanAPI:

    ADDRESS = test_addresses["XTZ"][0]
    REWARD_ADDRESS = test_addresses["XTZ"][1]

    def test_init(self):
        api = TzscanAPI(address=self.ADDRESS)
        assert api

    @mark.vcr()
    def test_get_balance(self):
        api = TzscanAPI(address=self.ADDRESS)
        result = api.get_balance()

        assert result == [{'symbol': 'XTZ', 'amount': 1221639.05003}]

    @mark.vcr()
    def test_get_rewards(self):
        api = TzscanAPI(address=self.ADDRESS)
        result = api.get_rewards()

        assert isinstance(result, list)
        # TODO: find better address, this one returns empty list

    @mark.vcr()
    def test_get_txs(self):
        api = TzscanAPI(address=self.ADDRESS)
        result = api.get_txs()

        assert isinstance(result, list)
        assert len(result) == 3

    @mark.vcr()
    def test_get_endorsements(self):
        api = TzscanAPI(address=self.ADDRESS)
        result = api.get_endorsements()

        assert isinstance(result, list)
        # TODO: find better address, this one returns empty list
