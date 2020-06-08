from pytest import mark, raises

from blockapi.api.dcrdata import DcrdataAPI
from blockapi.services import InternalServerError, AddressNotExist
from blockapi.test_init import test_addresses


class TestDcrdataAPI:

    ADDRESS = test_addresses["DCR"][0]

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
    def test_get_tx(self):
        hash_ = "193b59d8926588181aad5a5bed672e1fccf443f4d05dc1" \
                "6a0cdaacf3b4b4ed7c"
        api = DcrdataAPI(address=self.ADDRESS)
        result = api.get_tx(tx_hash=hash_)

        assert len(result) == 1


class TestResponse:

    text = None
    status_code = 200
