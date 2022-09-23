from datetime import datetime

import pytz

from blockapi.services import BlockchainAPI, set_default_args_values


class EtherscanAPI(BlockchainAPI):
    """
    Ethereum
    API docs: https://etherscan.io/apis
    Explorer: https://etherscan.io
    """

    symbol = 'ETH'
    base_url = 'https://api.etherscan.io'
    rate_limit = 0.2  # (5 req/sec)
    coef = 1e-18
    start_offset = 1
    max_items_per_page = 10000
    page_offset_step = 1

    supported_requests = {
        'get_balance': '/api?module=account&action=balance'
        '&address={address}&tag=latest&apikey={api_key}',
        'get_txs': '/api?module=account&action={action}&offset={offset}'
        '&sort={sort}&page={page}&address={address}'
        '&apikey={api_key}',
        'get_abi': '/api?module=contract&action=getabi&address={address}'
        '&apikey={api_key}',
    }

    def get_balance(self):
        balance_dict = self.request(
            'get_balance', address=self.address, api_key=self.api_key
        )

        # returns only balance for ETH; ERC20 and ERC721 tokens are omitted
        if 'result' in balance_dict:
            try:
                retval = int(balance_dict['result']) * self.coef
            except ValueError:
                return None
        else:
            return None

        return [{'symbol': self.symbol, 'amount': retval}]

    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        txs = self._get_txs('txlist', offset, limit)
        return [self.parse_tx(t, 'normal') for t in txs]

    def get_internal_txs(self, offset=None, limit=None, unconfirmed=False):
        txs = self._get_txs('txlistinternal', offset, limit)
        return [self.parse_tx(t, 'internal') for t in txs]

    def get_token_txs(self, offset=None, limit=None, unconfirmed=False):
        txs = self._get_txs('tokentx', offset, limit)
        return [self.parse_tx(t, 'token') for t in txs]

    def get_abi(self, contract):
        abi = self.request('get_abi', address=contract, api_key=self.api_key)

        return abi

    @set_default_args_values
    def _get_txs(self, action, offset=None, limit=None):
        response = self.request(
            'get_txs',
            action=action,
            offset=limit,
            sort='desc',
            page=offset,
            address=self.address,
            api_key=self.api_key,
        )

        if not response:
            return []
        result = response.get('result', [])
        if result is None:
            result = []

        status = response.get('status', '0')
        if status == '0':
            print('EtherscanAPI error: {}'.format(result))
            return []

        return result

    def parse_tx(self, tx, tx_type):
        direction = None
        if self.address.lower() == tx['from'].lower():
            direction = 'outgoing'
        elif self.address.lower() == tx['to'].lower():
            direction = 'incoming'
        elif not tx['contractAddress']:
            direction = 'outgoing'

        token_data = None
        if tx_type == 'token':
            token_data = {
                'name': tx.get('tokenName'),
                'symbol': tx.get('tokenSymbol'),
                'decimals': float(tx.get('tokenDecimal')),
            }
            symbol = token_data['symbol']
            amount = float(tx['value']) * pow(10, -token_data['decimals'])
        else:
            symbol = self.symbol
            amount = float(tx['value']) * self.coef

        return {
            'symbol': symbol,
            'date': datetime.fromtimestamp(int(tx['timeStamp']), pytz.utc),
            'from_address': tx['from'],
            'to_address': tx['to'],
            'contract_address': tx['contractAddress'],
            'amount': amount,
            'fee': float(tx.get('gasUsed', 0))
            * float(tx.get('gasPrice', 0))
            * self.coef,
            'gas': {
                'gas': float(tx['gas']),
                'gas_price': float(tx['gasPrice']) if tx.get('gasPrice') else None,
                'cumulative_gas_used': float(tx['cumulativeGasUsed'])
                if tx.get('cumulativeGasUsed')
                else None,
                'gas_used': float(tx['gasUsed']) if tx.get('gasUsed') else None,
            },
            'hash': tx['hash'],
            'confirmations': int(tx['confirmations'])
            if tx.get('confirmations')
            else None,
            'confirmed': None,
            'is_error': tx.get('isError') == '1',
            'type': tx_type,
            'kind': 'transaction',
            'direction': direction,
            'token_data': token_data,
            'raw': tx,
        }
