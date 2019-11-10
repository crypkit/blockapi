from web3 import Web3
import cfscrape
from bs4 import BeautifulSoup
import re
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
        self.infura_url = 'https://{}.infura.io/v3/{}'.format(self.network,
                                                              self.api_key)
        super().__init__(self.infura_url)


class ERC20Token:
    def __init__(self):
        self.url = 'https://etherscan.io/tokens?p={}'
        self.page = 0
        self.reqobj = cfscrape.create_scraper()
        self.tokens = {}

    @staticmethod
    def _get_number(num_string, rtype):
        """
        converts string in currency format $1234,56.78  or 1234.56 % into
        a user-defined type (usually float or int)

        :param num_string: string in US currency format / percentage
        :type num_string: string
        :param rtype: class to convert the resulting number to
        :type rtype: class
        :return: number converted from the string to the desired type
        """
        try:
            result = rtype(
                re.sub('[$,%]', '', num_string))
        except ValueError:
            result = None

        return result

    def get_token_list(self):
        """
        Scrapes the ERC20 token list from etherscan.io

        :return: dictionary containing currency_name, contract_addres,
                 price, change, volume, market_cap, holders - for each token
        :rtype: dict
        """
        while True:
            erc20_url = self.url.format(self.page)

            result = self.reqobj.get(erc20_url)

            if result.status_code == 200:
                soup = BeautifulSoup(result.text, "lxml")
                table = soup.body.find("table", {"id": "tblResult"})

                if table is None:
                    break

                table_body = table.find_all('tbody')[0]

                table_rows = table_body.find_all('tr')

                for row in table_rows:
                    row_ahref = row.find_all('a')[0]
                    cointext = row_ahref.text

                    coin_sc = row_ahref['href'][7:]

                    try:
                        currency_symbol = re.search('\([A-Za-z0-9]+\)',
                                                    cointext).group(0)[1:-1]
                    except AttributeError:
                        currency_symbol = cointext

                    currency_name = re.sub('\([A-Za-z0-9]+\)', '',
                                           cointext).strip()

                    row_tds = row.find_all('td')
                    row_tds[2].find('div').decompose()

                    currency_price = ERC20Token._get_number(row_tds[2].text,
                                                            float)
                    currency_change = ERC20Token._get_number(row_tds[3].text,
                                                             float)
                    currency_volume = ERC20Token._get_number(row_tds[4].text,
                                                             int)
                    market_cap = ERC20Token._get_number(row_tds[5].text, int)
                    holders = ERC20Token._get_number(row_tds[6].text, int)

                    self.tokens[currency_symbol] = \
                        {'currency_name': currency_name,
                         'contract_address': coin_sc,
                         'price': float(currency_price),
                         'change': currency_change,
                         'volume': currency_volume,
                         'market_cap': market_cap,
                         'holders': holders}

            else:
                break

            self.page += 1

        return self.tokens
