from web3 import Web3
import json
import requests
from blockapi.api import EtherscanAPI
from ethereum_input_decoder import AbiMethod


class Ethereum:
    def __init__(self, node_url):
        self.node_url = node_url
        self.web3 = Web3(Web3.HTTPProvider(self.node_url))
        self.abi = None

    def load_abi(self, contract):
        myapi = EtherscanAPI(contract)
        self.abi = myapi.get_abi(contract)['result']

    def toChecksumAddress(self, address):
        return self.web3.toChecksumAddress(address)

    def get_contract(self, contract):
        self.load_abi(contract)
        return self.web3.eth.contract(address=Web3.toChecksumAddress(
            contract), abi=self.abi)

    def get_tx_by_hash(self, txhash):
        tx = self.web3.eth.getTransaction(txhash)
        return tx

    def get_function_by_inputdata(self, tx_input):
        tx_input_decoded = AbiMethod.from_input_lookup(
            bytes.fromhex(tx_input[2:]))
        tx_input_values = list(tx_input_decoded.values())
        tx_function = tx_input_values[0]
        return tx_function


class Infura(Ethereum):
    def __init__(self, network, api_key):
        self.network = network
        self.api_prefix = network if network != "mainnet" else "api"
        self.api_key = api_key
        self.infura_url = 'https://{}.infura.io/v3/{}'.format(self.network,self.api_key)
        super().__init__(self.infura_url)
