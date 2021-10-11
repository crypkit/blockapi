from decimal import Decimal

from pytest import mark

from blockapi.api import SolanaApi
from blockapi.test_data import test_addresses


class TestSolanaAPI:
    ADDRESS = test_addresses['SOL'][0]

    @mark.vcr()
    def test_get_balance(self):
        api = SolanaApi(self.ADDRESS)
        result = api.get_balance()

        assert len(result) == 3
        assert next(b for b in result if b['symbol'] == 'SOL')
        assert next(b for b in result if b['symbol'] == 'UNKNOWN')
        usdt_bal = next(b for b in result if b['symbol'] == 'USDT')
        assert usdt_bal['amount'] == Decimal('21.17783')

    @mark.vcr()
    def test_get_txs_signatures(self):
        api = SolanaApi(self.ADDRESS)
        result = api.get_txs_signatures()

        assert len(result) == 22

    @mark.vcr()
    def test_get_tx(self):
        api = SolanaApi(self.ADDRESS)
        result = api.get_tx(
            '5v1yotDftqHWpgCqDuPoEMaLwyQiHaCiDZ3i2Srf31oKosDRJerk4PQpretG4HkQb'
            'WqRgfSFPLLdKi9NuyGLcqQH'
        )

        assert result
