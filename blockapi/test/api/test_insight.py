from pytest import mark

from blockapi.api.insight import RavencoinAPI
from blockapi.test_init import test_addresses


class TestInsightAPI:
    RAVEN_ADDRESS = test_addresses['RVN'][1]

    @mark.vcr()
    def test_get_balance_raven_coin(self):
        api = RavencoinAPI(address=self.RAVEN_ADDRESS)
        result = api.get_balance()

        assert result == 957.0026321
