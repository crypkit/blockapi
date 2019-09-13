import itertools
import unittest

import blockapi
import blockapi.api
from blockapi.services import AddressNotExist, APIError, BadGateway, GatewayTimeOut, InternalServerError

test_addresses = {
    'bitcoin': [
        '1NuXUAnkWBYF3Fs9CkjfARYMacrVtoCrAM',
        'ypub6WjHjrJLKSg8oQw1E4LGvQDJ2uofgMfJKLnv5Ha4NPRW4rf7LPXffMJ8EReixY1mUCc33SsiDUodUCTvCktFeN7ZW28GVhBXhNnoKYUqXbP',
        'xpub6CUGRUonZSQ4TWtTMmzXdrXDtypWKiKrhko4egpiMZbpiaQL2jkwSB1icqYh2cfDfVxdx4df189oLKnC5fSwqPfgyP3hooxujYzAu3fDVmz'
    ],
    'bitcoin-cash': [
        '35hK24tcLEWcgNA4JxpvbkNkoAcDGqQPsP',
    ],
    'cardano': [
        'DdzFFzCqrhsdyjuJWYcfEWSuk4TB25HGv66bQKeU3KpvA78xfDbgu1rQdhaLHb5XvqPU7gfKS5mBoGmRNNhTSQ3H7iL1so8RygHMdNiN'
    ],
    'eos': [],
    'ethereum': [
        '0x1d0DcC8d8BcaFa8e8502BEaEeF6CBD49d3AFFCDC'
    ],
    'litecoin': [
        # 'MBuTKxJaHMN3UsRxQqpGRPdA7sCfE1UF7n',
        '3QY7aJKtRHDy3a8V5RS99A813hie9YqjhF'
    ],
    'tezos': [
        'tz1bDXD6nNSrebqmAnnKKwnX1QdePSMCj4MX'
    ],
    'decred': [
        'DsXt3he1A9KB2uL1g3MJvbAbXEB1CxN2rNF'
        # current api doesn't support xpub key
        # 'dpubZFwoKEEJYVDxGo8bf2E4qwh6Qve9cku5gvaS5kC96hUdMT7SF9nymaLFeEFQaHy8a3SuiUJRL87rz3bfwFSFqErYVeHUg3xnzPjHftiofFu',
    ],
    'cosmos': [
        'cosmos1gn326f6sza44xt5kxrsdrnapp2sxhav03rhcsz'
    ],
    'neocoin': [
        'AZnTM3mYbx9yzg8tb6hr7w9pAKntDmrtqk'
    ],
    'dogecoin': [
        'DH5yaieqoZN36fDVciNyRueRGvGLR3mr7L'
    ],
    'zcash': [
        't1fLdzB7mHQgdb3tD474V9wYtuknPfQSX5e'
    ],
    'dashcoin': [
        'XtAG1982HcYJVibHxRZrBmdzL5YTzj4cA1'
    ],
    'ethereum-classic': [
        '0x9d2BFC36106F038250c01801685785b16C86C60D'
    ],
    'horizen': [
        'znZTLu1asaLWxB7EBqBRQ6DCnNyctYA3Rm4'
    ],
}

test_invalid_addresses = {
    'bitcoin': ['xxxx', ],
    'bitcoin-cash': ['xxxx', ],
    'cardano': ['xxxx', ],
    'eos': [],
    'ethereum': ['xxxx', ],
    'litecoin': ['xxxx', ],
    'tezos': ['xxxx', ],
    'decred': ['xxxx', ],
    'cosmos': ['xxxx', ],
    'neocoin': ['xxxx', ],
    'dogecoin': ['xxxx', ],
    'zcash': ['xxxx', ],
    'dashcoin': ['xxxx', ],
    'ethereum-classic': ['xxxx', ],
    'horizen': ['xxxx', ],
}


class BlockapiTestCase(unittest.TestCase):
    currencies = ('bitcoin', 'bitcoin-cash', 'cardano',
                  'eos', 'ethereum', 'litecoin', 'tezos',
                  'decred', 'cosmos', 'neocoin', 'dogecoin',
                  'zcash', 'dashcoin', 'ethereum-classic',
                  'horizen')

    def test_valid_address(self):
        for currency_id in self.currencies:
            with self.subTest(currency_id):
                api_classes = blockapi.get_api_classes_for_coin(currency_id)
                addresses = test_addresses[currency_id]

                for api_class, address in itertools.product(api_classes, addresses):
                    api_inst = api_class(address)
                    try:
                        b = api_inst.get_balance()
                    except (AddressNotExist, BadGateway, GatewayTimeOut, InternalServerError, APIError):
                        self.fail("get_balance for {} [{}] failed unexpectedly with a valid address {}".format(
                            api_inst.__class__.__name__, currency_id, address))

    def test_invalid_address(self):
        for currency_id in self.currencies:
            with self.subTest(currency_id):
                api_classes = blockapi.get_api_classes_for_coin(currency_id)
                addresses = test_invalid_addresses[currency_id]

                for api_class, address in itertools.product(api_classes, addresses):
                    try:
                        api_inst = api_class(address)
                    except ValueError:
                        pass
                    else:
                        with self.assertRaises(
                                (blockapi.services.AddressNotExist, blockapi.services.APIError),
                                msg="API/currency: {}/{}".format(api_inst.__class__.__name__,
                                                                 currency_id)):
                            b = api_inst.get_balance()

    def test_get_balance(self):
        for currency_id in self.currencies:
            with self.subTest(currency_id):
                api_classes = blockapi.get_api_classes_for_coin(currency_id)
                addresses = test_addresses[currency_id]

                for api_class, address in itertools.product(api_classes, addresses):
                    api_inst = api_class(address)
                    try:
                        b = api_inst.get_balance()
                    except:
                        self.fail("get_balance for {} [{}] failed unexpectedly".format(api_inst.__class__.__name__,
                                                                                       currency_id))

                    try:
                        tmp = float(b)
                    except (ValueError, TypeError):
                        self.fail("get_balance for {} [{}] failed unexpectedly - returned value is not a number".format(
                            api_inst.__class__.__name__, currency_id))

                    # if currency_id == 'cosmos':
                    #    # get both incoming and outgoing transactions
                    #    it = api_inst.get_incoming_txs()
                    #    ot = api_inst.get_outgoing_txs()
                    # else:
                    #    # get transactions
                    #    t = api_inst.get_txs()

    def test_random_balance(self):
        for currency_id in self.currencies:
            with self.subTest(currency_id):
                addresses = test_addresses[currency_id]
                for address in addresses:
                    try:
                        blockapi.get_balance_from_random_api(currency_id, address)
                    except:
                        self.fail("get_balance_from_random_api for {} failed unexpectedly".format(currency_id))


if __name__ == "__main__":
    unittest.main()
