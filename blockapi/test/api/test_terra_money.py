from decimal import Decimal

from pytest import mark

from blockapi.api.terra_money import TerraMoneyApi
from blockapi.test_data import test_addresses


class TestTerraMoneyApi:
    ADDRESS = test_addresses["LUNA"][0]

    def test_init(self):
        api = TerraMoneyApi(address=self.ADDRESS)
        assert api

    @mark.vcr()
    def test_get_balance(self):
        api = TerraMoneyApi(address=self.ADDRESS)
        result = api.get_balance()

        assert result == [
            {'symbol': 'LUNA', 'amount': Decimal('34682.501828')},
            {'symbol': 'KRT', 'amount': Decimal('9412.963717')},
            {'symbol': 'SDT', 'amount': Decimal('0.052803')},
            {'symbol': 'UST', 'amount': Decimal('0.012112')},
            {'symbol': 'MNT', 'amount': Decimal('1122.501887')},
        ]

    @mark.vcr()
    def test_get_txs(self):
        api = TerraMoneyApi(address=self.ADDRESS)
        result = api.get_txs()

        assert len(result) == 11

    @mark.vcr()
    def test_get_delegations(self):
        api = TerraMoneyApi(address=self.ADDRESS)
        result = api.get_delegations()

        assert result
