import itertools
import unittest

import blockapi
import blockapi.api
from blockapi.services import AddressNotExist, APIError, BadGateway, GatewayTimeOut, InternalServerError

test_addresses = {
    'BTC': [
        '1NuXUAnkWBYF3Fs9CkjfARYMacrVtoCrAM',
        'ypub6WjHjrJLKSg8oQw1E4LGvQDJ2uofgMfJKLnv5Ha4NPRW4rf7LPXffMJ8EReixY1mUCc33SsiDUodUCTvCktFeN7ZW28GVhBXhNnoKYUqXbP',
        'xpub6CUGRUonZSQ4TWtTMmzXdrXDtypWKiKrhko4egpiMZbpiaQL2jkwSB1icqYh2cfDfVxdx4df189oLKnC5fSwqPfgyP3hooxujYzAu3fDVmz'
    ],
    'BCH': [
        '35hK24tcLEWcgNA4JxpvbkNkoAcDGqQPsP',
    ],
    'ADA': [
        'DdzFFzCqrhsdyjuJWYcfEWSuk4TB25HGv66bQKeU3KpvA78xfDbgu1rQdhaLHb5XvqPU7gfKS5mBoGmRNNhTSQ3H7iL1so8RygHMdNiN'
    ],
    'EOS': [],
    'ETH': [
        '0x1d0DcC8d8BcaFa8e8502BEaEeF6CBD49d3AFFCDC'
    ],
    'LTC': [
        # 'MBuTKxJaHMN3UsRxQqpGRPdA7sCfE1UF7n',
        '3QY7aJKtRHDy3a8V5RS99A813hie9YqjhF'
    ],
    'XTZ': [
        'tz1bDXD6nNSrebqmAnnKKwnX1QdePSMCj4MX'
    ],
    'DCR': [
        'DsXt3he1A9KB2uL1g3MJvbAbXEB1CxN2rNF'
        # current api doesn't support xpub key
        # 'dpubZFwoKEEJYVDxGo8bf2E4qwh6Qve9cku5gvaS5kC96hUdMT7SF9nymaLFeEFQaHy8a3SuiUJRL87rz3bfwFSFqErYVeHUg3xnzPjHftiofFu',
    ],
    'ATOM': [
        'cosmos1gn326f6sza44xt5kxrsdrnapp2sxhav03rhcsz'
    ],
    'NEO': [
        'AZnTM3mYbx9yzg8tb6hr7w9pAKntDmrtqk'
    ],
    'DOGE': [
        'DH5yaieqoZN36fDVciNyRueRGvGLR3mr7L'
    ],
    'ZEC': [
        't1fLdzB7mHQgdb3tD474V9wYtuknPfQSX5e'
    ],
    'DASH': [
        'XtAG1982HcYJVibHxRZrBmdzL5YTzj4cA1'
    ],
    'ETC': [
        '0x9d2BFC36106F038250c01801685785b16C86C60D'
    ],
    'ZEN': [
        'znZTLu1asaLWxB7EBqBRQ6DCnNyctYA3Rm4'
    ],
}

test_invalid_addresses = {
    'BTC': ['xxxx', ],
    'BCH': ['xxxx', ],
    'ADA': ['xxxx', ],
    'EOS': [],
    'ETH': ['xxxx', ],
    'LTC': ['xxxx', ],
    'XTZ': ['xxxx', ],
    'DCR': ['xxxx', ],
    'ATOM': ['xxxx', ],
    'NEO': ['xxxx', ],
    'DOGE': ['xxxx', ],
    'ZEC': ['xxxx', ],
    'DASH': ['xxxx', ],
    'ETC': ['xxxx', ],
    'ZEN': ['xxxx', ],
}


class BlockapiTestCase(unittest.TestCase):
    currencies = test_addresses.keys()

    def test_valid_address(self):
        for symbol in self.currencies:
            with self.subTest(symbol):
                api_classes = blockapi.get_api_classes_for_coin(symbol)
                addresses = test_addresses[symbol]

                for api_class, address in itertools.product(api_classes, addresses):
                    api_inst = api_class(address)
                    try:
                        b = api_inst.get_balance()
                    except (AddressNotExist, BadGateway, GatewayTimeOut, InternalServerError, APIError):
                        self.fail("get_balance for {} [{}] failed unexpectedly with a valid address {}".format(
                            api_inst.__class__.__name__, symbol, address))

    def test_invalid_address(self):
        for symbol in self.currencies:
            with self.subTest(symbol):
                api_classes = blockapi.get_api_classes_for_coin(symbol)
                addresses = test_invalid_addresses[symbol]

                for api_class, address in itertools.product(api_classes, addresses):
                    try:
                        api_inst = api_class(address)
                    except ValueError:
                        pass
                    else:
                        with self.assertRaises(
                                (blockapi.services.AddressNotExist, blockapi.services.APIError),
                                msg="API/currency: {}/{}".format(api_inst.__class__.__name__,
                                                                 symbol)):
                            b = api_inst.get_balance()

    def test_get_balance(self):
        for symbol in self.currencies:
            with self.subTest(symbol):
                api_classes = blockapi.get_api_classes_for_coin(symbol)
                addresses = test_addresses[symbol]

                for api_class, address in itertools.product(api_classes, addresses):
                    api_inst = api_class(address)
                    try:
                        b = api_inst.get_balance()
                    except:
                        self.fail("get_balance for {} [{}] failed unexpectedly".format(api_inst.__class__.__name__,
                                                                                       symbol))

                    try:
                        tmp = float(b)
                    except (ValueError, TypeError):
                        self.fail("get_balance for {} [{}] failed unexpectedly - returned value is not a number".format(
                            api_inst.__class__.__name__, symbol))

                    # if symbol == 'cosmos':
                    #    # get both incoming and outgoing transactions
                    #    it = api_inst.get_incoming_txs()
                    #    ot = api_inst.get_outgoing_txs()
                    # else:
                    #    # get transactions
                    #    t = api_inst.get_txs()

    def test_random_balance(self):
        for symbol in self.currencies:
            with self.subTest(symbol):
                addresses = test_addresses[symbol]
                for address in addresses:
                    try:
                        blockapi.get_balance_from_random_api(symbol, address)
                    except:
                        self.fail("get_balance_from_random_api for {} failed unexpectedly".format(symbol))

    def test_rate_limits(self):
        for symbol in self.currencies:
            with self.subTest(symbol):
                addresses = test_addresses[symbol]
                for address in addresses:
                    for _ in range(2):
                        try:
                            blockapi.get_balance_from_random_api(symbol, address)
                        except _:
                            self.fail("repeated call for {} failed unexpectedly".format(symbol))


# TODO check obligatory fields in response
def check_obligatory_fields(method, args, kwargs, obligatory_fields):
    response = method(*args, **kwargs)
    if not response:
        return True

    response_keys = []
    if type(response) == dict:
        response_keys = response.keys
    elif type(response) == list:
        response_keys = response[0].keys

    missing_fields = []
    for obl_field in obligatory_fields:
        if obl_field not in response_keys:
            missing_fields.append(obl_field)


if __name__ == "__main__":
    unittest.main()
