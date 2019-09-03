from .services import (
    TzscanAPI, DcrdataAPI, CosmosAPI, EosparkAPI
)
#from backend.accounts.blockchains.ethereum import Ethereum
#from backend.accounts.blockchains.tezos import Tezos
from blockapi import get_api_classes_for_coin

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

def test_bitcoin_api():
    _test_blockchain_api('bitcoin')

def test_cardano_api():
    _test_blockchain_api('cardano')

def test_eos_api():
    _test_blockchain_api('eos')

def test_ethereum_api():
    _test_blockchain_api('etherem')

def test_litecoin_api():
    _test_blockchain_api('litecoin')

def test_tezos_api():
    _test_blockchain_api('tezos')

def test_decred_api():
    _test_blockchain_api('decred')

def test_cosmos_api():
    api_classes = get_api_classes_for_coin('cosmos')
    addresses = test_addresses['cosmos']

    for api_class, address in itertools.product(api_classes, addresses):
        api_inst = api_class(address)
        b = api_inst.get_balance()
        it = api_inst.get_incoming_txs()
        ot = api_inst.get_outgoing_txs()
        # just for check values in debugging
        b,it,ot = b,it,ot

def _test_blockchain_api(currency_id):
    """Test always all test addresses with all available apis."""

    api_classes = get_api_classes_for_coin(currency_id)
    addresses = test_addresses[currency_id]

    for api_class, address in itertools.product(api_classes, addresses):
        api_inst = api_class(address)
        b = api_inst.get_balance()
        t = api_inst.get_txs()
        # just for check values in debugging
        b,t = b,t


if __name__ == "__main__":
    # test_cardano_api()
    # test_eos_api()
    # test_ethereum_api()
    # test_tezos_api()
    # test_decred_api()
    # test_cosmos_api()
    test_litecoin_api()

    # for i in range(100):
    #     print('{} call'.format(i+1))
    #     # test_bitcoin_api()
 