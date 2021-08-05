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
    def test_get_staked(self):
        api = TerraMoneyApi(address=self.ADDRESS)
        result = api.get_staked()

        assert result == {'symbol': 'LUNA', 'amount': Decimal('10369.62345099999953075495919')}


    @mark.vcr()
    def test_get_rewards(self):
        api = TerraMoneyApi(address=self.ADDRESS)
        result = api.get_rewards()

        assert result == [
            {
                'amount': Decimal('13.24497999999999940063964617'), 'symbol': 'LUNA'
            },
            {
                'amount': Decimal('8120.888700999999632514452628'), 'symbol': 'KRT'
            },
            {
                'amount': Decimal('0.05828099999999999736267470532'), 'symbol': 'SDT'
            },
            {
                'amount': Decimal('7.819931999999999646133311607'), 'symbol': 'UST'
            },
            {
                'amount': Decimal('0.00002199999999999999900445846017'), 'symbol': 'CAT'
            },
            {
                'amount': Decimal('0.00007399999999999999665136027512'), 'symbol': 'CHT'
            },
            {
                'amount': Decimal('9.999999999999999547481118259E-7'), 'symbol': 'CNT'
            },
            {
                'amount': Decimal('0.00006299999999999999714913104503'), 'symbol': 'EUT'
            },
            {
                'amount': Decimal('0.000007999999999999999637984894607'), 'symbol': 'GBT'
            },
            {
                'amount': Decimal('0.000007999999999999999637984894607'), 'symbol': 'HKT'
            },
            {
                'amount': Decimal('0.0002409999999999999890942949500'), 'symbol': 'INT'
            },
            {
                'amount': Decimal('0.004759999999999999784601012291'), 'symbol': 'JPT'
            },
            {
                'amount': Decimal('289.3361699999999869069919904'), 'symbol': 'MNT'
            },
            {
                'amount': Decimal('0.00002999999999999999864244335478'), 'symbol': 'SET'
            },
            {
                'amount': Decimal('0.0002289999999999999896373176081'), 'symbol': 'THT'
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
