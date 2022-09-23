import re
from time import sleep

import cfscrape
import requests
from bs4 import BeautifulSoup
from ethereum_input_decoder import AbiMethod
from web3 import Web3

from blockapi.api import EtherscanAPI


class Ethereum:
    def __init__(self, node_url, etherscan_api_key):
        self.node_url = node_url
        self.etherscan_api_key = etherscan_api_key
        self.web3 = Web3(Web3.HTTPProvider(self.node_url))
        self.abi = None

    def load_abi(self, contract):
        myapi = EtherscanAPI(contract, api_key=self.etherscan_api_key)
        self.abi = myapi.get_abi(contract)['result']

    def to_checksum_addr(self, address):
        return self.web3.toChecksumAddress(address)

    def get_contract(self, contract):
        # fallback to automatic loading if ABI is not set from outside
        if self.abi is None:
            self.load_abi(contract)
        return self.web3.eth.contract(
            address=Web3.toChecksumAddress(contract), abi=self.abi
        )

    def get_tx_by_hash(self, txhash):
        tx = self.web3.eth.getTransaction(txhash)
        return tx

    @staticmethod
    def get_function_by_inputdata(tx_input):
        tx_input_decoded = AbiMethod.from_input_lookup(bytes.fromhex(tx_input[2:]))
        tx_input_values = list(tx_input_decoded.values())
        tx_function = tx_input_values[0]
        return tx_function

    def get_erc20_balances(self, address, tokens: dict):
        addr = '0xD1f89108Ba9525a11BEAf8bdC5058B4946a6C501'
        addr = Web3.toChecksumAddress(addr)
        address = Web3.toChecksumAddress(address)

        tokens_ch = []
        for token in tokens:
            tokens_ch.append(Web3.toChecksumAddress(tokens[token]['contract_address']))

        bal_sc = self.get_contract(addr)
        balances = bal_sc.functions.batchTokenBalances([address], tokens_ch).call()

        decimals = [tokens[token]['decimals'] for token in tokens]
        symbols = [token for token in tokens]
        contract_addresses = [tokens[token]['contract_address'] for token in tokens]

        return [
            {'amount': float(b) * pow(10, -d), 'symbol': symbol, 'contract_address': sc}
            for b, d, symbol, sc in zip(balances, decimals, symbols, contract_addresses)
            if b > 0
        ]


class Infura(Ethereum):
    def __init__(self, network, api_key, etherscan_api_key):
        self.network = network
        self.api_prefix = network if network != "mainnet" else "api"
        self.api_key = api_key
        self.etherscan_api_key = etherscan_api_key
        self.infura_url = 'https://{}.infura.io/v3/{}'.format(
            self.network, self.api_key
        )
        super().__init__(self.infura_url, etherscan_api_key)


class ERC20Token:
    def __init__(self):
        self.url = 'https://etherscan.io/tokens?p={}'
        self.token_url = 'https://etherscan.io/token/{}'
        self.page = 0
        self.reqobj = cfscrape.create_scraper()
        self.tokens = {}

    def get_token_list(self):
        """
        Scrapes the ERC20 token list from etherscan.io

        :return: dictionary containing currency_name, contract_addres,
                 price, change, volume, market_cap, holders - for each token
        :rtype: dict
        """
        scrape_result = True
        result_msg = ''
        page = 0

        while True:
            status_code, rows = self._get_table_rows(page)
            if status_code != 200:
                scrape_result = False
                result_msg = 'error {} on page {}'.format(status_code, page)
                break

            if rows is None:
                break

            for row in rows:
                result = self._parse_table_row(row)
                decimals = self._get_token_details(result[2])

                self.tokens[result[0]] = {
                    'currency_name': result[1],
                    'contract_address': result[2],
                    'price': float(result[3]),
                    'change': result[4],
                    'volume': result[5],
                    'market_cap': result[6],
                    'holders': result[7],
                    'decimals': decimals,
                }

            page += 1

        return {
            'result': scrape_result,
            'result_msg': result_msg,
            'tokens': self.tokens,
        }

    def _get_token_details(self, contract_address):
        token_details_url = self.token_url.format(contract_address)
        i = 1
        while True:
            try:
                result = self.reqobj.get(token_details_url)
                if result.text.find('Sorry, You have reached') != -1:
                    i += 1
                    sleep(0.3 * i)
                    continue
                break
            except requests.exceptions.ChunkedEncodingError:
                i += 1

            sleep(0.3 * i)

        if result.status_code != 200:
            return None

        soup = BeautifulSoup(result.text, "lxml")
        decimals_div = soup.body.find("div", {"id": "ContentPlaceHolder1_trDecimals"})
        if decimals_div is None:
            return None

        decimals_class = decimals_div.find("div", {"class": "col-md-8"})
        return int(decimals_class.text)

    def _get_table_rows(self, page):
        erc20_url = self.url.format(page)
        i = 1
        while True:
            try:
                result = self.reqobj.get(erc20_url)
                if result.text.find('Sorry, You have reached') != -1:
                    i += 1
                    sleep(0.3 * i)
                    continue
                break
            except requests.exceptions.ChunkedEncodingError:
                i += 1

            sleep(0.3 * i)

        if result.status_code == 200:
            soup = BeautifulSoup(result.text, "lxml")
            table = soup.body.find("table", {"id": "tblResult"})

            if table is None:
                return result.status_code, None

            table_body = table.find_all('tbody')[0]
            table_rows = table_body.find_all('tr')

            return result.status_code, table_rows
        else:
            return result.status_code, None

    def _parse_table_row(self, row):
        row_ahref = row.find_all('a')[0]
        cointext = row_ahref.text

        coin_sc = row_ahref['href'][7:]
        currency_symbol = self._get_currency_symbol(cointext)
        currency_name = self._get_currency_name(cointext)

        row_tds = row.find_all('td')
        row_tds[2].find('div').decompose()

        currency_price = ERC20Token._get_number(row_tds[2].text, float)
        currency_change = ERC20Token._get_number(row_tds[3].text, float)
        currency_volume = ERC20Token._get_number(row_tds[4].text, int)
        market_cap = ERC20Token._get_number(row_tds[5].text, int)
        holders = ERC20Token._get_number(row_tds[6].text, int)

        return (
            currency_symbol,
            currency_name,
            coin_sc,
            currency_price,
            currency_change,
            currency_volume,
            market_cap,
            holders,
        )

    @staticmethod
    def _get_currency_symbol(cointext):
        try:
            currency_symbol = re.search('\([A-Za-z0-9]+\)', cointext).group(0)[1:-1]
        except AttributeError:
            currency_symbol = cointext

        return currency_symbol

    @staticmethod
    def _get_currency_name(cointext):
        currency_name = re.sub('\([A-Za-z0-9]+\)', '', cointext).strip()
        return currency_name

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
            result = rtype(re.sub('[$,%]', '', num_string))
        except ValueError:
            result = None

        return result

    def get_contract_by_symbol(self, symbol):
        if len(self.tokens) == 0:
            return None

        if self.tokens.get(symbol) is not None:
            return self.tokens[symbol]['contract_address']
        else:
            return None
