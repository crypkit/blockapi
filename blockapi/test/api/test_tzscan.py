from pytest import mark

from blockapi.api.tzscan import TzscanAPI
from blockapi.test_init import test_addresses


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

        assert result == [{'symbol': 'XTZ', 'amount': 2068856.4582429999}]

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
    def test_get_bakings_tzstats(self):
        api = TzscanAPI(address=self.REWARD_ADDRESS)
        result = api.get_bakings_tzstats()

        assert result["address"] == self.REWARD_ADDRESS
        assert "manager" in result
        assert "delegate" in result
        assert "manager_account" in result
        assert "delegate_account" in result

    @mark.vcr()
    def test_get_endorsements(self):
        api = TzscanAPI(address=self.ADDRESS)
        result = api.get_endorsements()

        assert isinstance(result, list)
        # TODO: find better address, this one returns empty list
