from decimal import Decimal
from pytest import mark

from blockapi.api.terra_money import TerraMoneyApi

from blockapi.test_init import test_addresses


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
            {
                'symbol': 'LUNA',
                'amount': Decimal('33890.58385199999846638708938')
            },
            {
                'symbol': 'KRT',
                'amount': Decimal('53220.06604899999759169152253')
            },
            {
                'symbol': 'SDT',
                'amount': Decimal('0.01246999999999999943570895447')
            },
            {
                'symbol': 'UST',
                'amount': Decimal('0.00004999999999999999773740559129')
            },
            {
                'symbol': 'MNT',
                'amount': Decimal('112.7350019999999948985282962')
            }
        ]

    @mark.vcr()
    def test_get_txs(self):
        api = TerraMoneyApi(address=self.ADDRESS)
        result = api.get_txs()

        assert len(result) == 5

    @mark.vcr()
    def test_get_delegations(self):
        api = TerraMoneyApi(address=self.ADDRESS)
        result = api.get_delegations()

        assert result
