from decimal import Decimal

from pytest import mark

from blockapi.api.terra_money import TerraMoneyApi
from blockapi.test.test_data import test_addresses


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
                'amount': Decimal('34682.50182799999843055130568')
            },
            {
                'symbol': 'KRT',
                'amount': Decimal('9412.963716999999574045618491')
            },
            {
                'symbol': 'SDT',
                'amount': Decimal('0.05280299999999999761056454874')
            },
            {
                'symbol': 'UST',
                'amount': Decimal('0.01211199999999999945190913044')
            },
            {
                'symbol': 'MNT',
                'amount': Decimal('1122.501886999999949204670134')
            }
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
