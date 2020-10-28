from pytest import mark, raises

from blockapi.api.cosmos import CosmosAPI
from blockapi.services import AddressNotExist, InternalServerError
from blockapi.test_data import test_addresses


class TestCosmosAPI:
    ADDRESS = test_addresses["ATOM"][0]

    def test_init(self):
        api = CosmosAPI(address=self.ADDRESS)
        assert api

    def test_process_error_response(self):
        response = TestResponse()

        response.text = "Error"
        response.status_code = 500

        with raises(InternalServerError):
            CosmosAPI(address=self.ADDRESS).process_error_response(response)

        response.text = "Error decoding bech32 failed"

        with raises(AddressNotExist):
            CosmosAPI(address=self.ADDRESS).process_error_response(response)

    @mark.vcr()
    def test_get_info(self):
        api = CosmosAPI(address=self.ADDRESS)
        result = api.get_info()

        assert "result" in result
        assert "value" in result["result"]
        assert "address" in result["result"]["value"]
        assert "coins" in result["result"]["value"]
        assert isinstance(result["result"]["value"]["coins"], list)
        assert "denom" in result["result"]["value"]["coins"][0]
        assert "amount" in result["result"]["value"]["coins"][0]
        assert "account_number" in result["result"]["value"]
        assert "sequence" in result["result"]["value"]

    @mark.vcr()
    def test_get_balance(self):
        api = CosmosAPI(address=self.ADDRESS)
        result = api.get_balance()

        assert result == [{"symbol": "ATOM", "amount": 0.005959}]

    @mark.vcr()
    def test_get_incoming_txs(self):
        api = CosmosAPI(address=self.ADDRESS)
        api.get_incoming_txs()

        # TODO: provider is not sending correct data

    @mark.vcr()
    def test_get_outgoing_txs(self):
        api = CosmosAPI(address=self.ADDRESS)
        api.get_outgoing_txs()

        # TODO: provider is not sending correct data


class TestResponse:

    text = None
    status_code = 200
