from pytest import mark, raises

from blockapi.api.dcrdata import DcrdataAPI
from blockapi.services import InternalServerError, AddressNotExist
from blockapi.test_init import test_addresses


class TestDcrdataAPI:

    ADDRESS = test_addresses["DCR"][0]
    STAKING_ADDRESS = test_addresses["DCR"][1]

    def test_init(self):
        api = DcrdataAPI(address=self.ADDRESS)
        assert api

    def test_process_error_response(self):
        response = TestResponse()

        response.text = "Error"
        response.status_code = 500

        with raises(InternalServerError):
            DcrdataAPI(address=self.ADDRESS).process_error_response(response)

        response.status_code = 422

        with raises(AddressNotExist):
            DcrdataAPI(address=self.ADDRESS).process_error_response(response)

    @mark.vcr()
    def test_get_balance(self):
        api = DcrdataAPI(address=self.ADDRESS)
        result = api.get_balance()

        assert result == [{'symbol': 'DCR', 'amount': 135.0176}]

    @mark.vcr()
    def test_get_txs(self):
        api = DcrdataAPI(address=self.ADDRESS)
        result = api.get_txs(limit=2)

        assert len(result) == 2
        assert all(k in ["kind", "result"] for k in result[0].keys())

    @mark.vcr()
    def test_get_txs_staking(self):
        api = DcrdataAPI(address=self.STAKING_ADDRESS)
        result = api.get_txs()

        assert isinstance(result, list)
        assert len(result) == 21
        assert result[0]["kind"] == "ticket"
        assert result[0]["result"]["hash"] == "51f27646cd8b98873816d820281bb"\
            "bf850de79564440e3b18eceef46ef56cfae"
        assert result[0]["result"]["purchased_on"].year == 2020
        assert result[0]["result"]["purchased_on"].month == 6
        assert result[0]["result"]["purchased_on"].day == 5
        assert result[0]["result"]["investment"] == 146.59688866
        assert result[0]["result"]["ticket_cost"] == 146.59683446
        assert result[0]["result"]["transaction_fee"] == 5.419999999389802e-05
        assert result[0]["result"]["pool_fee"] == 0.0087343
        assert result[0]["result"]["status"] == "live"

    @mark.vcr()
    def test_get_tx(self):
        hash_ = "193b59d8926588181aad5a5bed672e1fccf443f4d05dc1" \
                "6a0cdaacf3b4b4ed7c"
        api = DcrdataAPI(address=self.ADDRESS)
        result = api.get_tx(tx_hash=hash_)

        assert len(result) == 1


class TestResponse:

    text = None
    status_code = 200
