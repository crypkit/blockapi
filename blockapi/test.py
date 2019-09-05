import unittest
import blockapi
from blockapi.services import AddressNotExist,APIError,BadGateway,GatewayTimeOut
import blockapi.api
import itertools

test_addresses = {
    'bitcoin': [
        '1NuXUAnkWBYF3Fs9CkjfARYMacrVtoCrAM',
        'ypub6WjHjrJLKSg8oQw1E4LGvQDJ2uofgMfJKLnv5Ha4NPRW4rf7LPXffMJ8EReixY1mUCc33SsiDUodUCTvCktFeN7ZW28GVhBXhNnoKYUqXbP',
        'xpub6CUGRUonZSQ4TWtTMmzXdrXDtypWKiKrhko4egpiMZbpiaQL2jkwSB1icqYh2cfDfVxdx4df189oLKnC5fSwqPfgyP3hooxujYzAu3fDVmz'
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
    ]
}

test_invalid_addresses = {
    'bitcoin': [ 'xxxx', ],
    'cardano': [ 'xxxx', ],
    'eos': [],
    'ethereum': [ 'xxxx', ],
    'litecoin': [ 'xxxx', ],
    'tezos': [ 'xxxx', ],
    'decred': [ 'xxxx', ],
    'cosmos': [ 'xxxx', ]
}

class BlockapiTestCase(unittest.TestCase):
    currencies = ('bitcoin', 'cardano', 'eos', 'ethereum', 'litecoin', 'tezos', 'decred', 'cosmos')


    def test_valid_address(self):
        for currency_id in self.currencies:
            with self.subTest(currency_id):
                api_classes = blockapi.get_api_classes_for_coin(currency_id)
                addresses = test_addresses[currency_id]

                for api_class, address in itertools.product(api_classes, addresses):
                    api_inst = api_class(address)
                    try:
                        b = api_inst.get_balance()
                    except (AddressNotExist,BadGateway,GatewayTimeOut,APIError):
                        self.fail("get_balance for {} [{}] failed unexpectedly with a valid address {}".format(api_inst.__class__.__name__,currency_id,address))

    def test_invalid_address(self):
        for currency_id in self.currencies:
            with self.subTest(currency_id):
                api_classes = blockapi.get_api_classes_for_coin(currency_id)
                addresses = test_invalid_addresses[currency_id]

                for api_class, address in itertools.product(api_classes, addresses):
                    api_inst = api_class(address)
                    with self.assertRaises((blockapi.services.AddressNotExist,
                                            blockapi.services.APIError),
                                            msg="API/currency: {}/{}".format(api_inst.__class__.__name__, currency_id)):
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
                        self.fail("get_balance for {} [{}] failed unexpectedly".format(api_inst.__class__.__name__,currency_id))

                    try:
                        tmp = float(b)
                    except (ValueError,TypeError):
                        self.fail("get_balance for {} [{}] failed unexpectedly - returned value is not a number".format(api_inst.__class__.__name__,currency_id))

                    #if currency_id == 'cosmos':
                    #    # get both incoming and outgoing transactions
                    #    it = api_inst.get_incoming_txs()
                    #    ot = api_inst.get_outgoing_txs()
                    #else:
                    #    # get transactions
                    #    t = api_inst.get_txs()

if __name__ == "__main__":
    unittest.main()
