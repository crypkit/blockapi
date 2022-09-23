import dateutil.parser

from blockapi.services import BlockchainAPI


class EosparkAPI(BlockchainAPI):
    """
    EOS
    API docs: https://developer.eospark.com/api-doc/https/
    Explorer: https://eospark.com
    """

    symbol = 'EOS'
    base_url = 'https://api.eospark.com/api'
    rate_limit = 0
    coef = 1e-6
    max_items_per_page = 20
    page_offset_step = 1

    supported_requests = {
        'get_balance': '?module=account&action=get_account_balance'
        '&apikey={api_key}&account={address}',
        'get_token_balances': '?module=account&action=get_token_list'
        '&apikey={api_key}&account={address}',
        'get_txs': '?module=account&action=get_account_related_trx_info'
        '&apikey={api_key}&account={address}'
        '&page={page}&size={size}',
    }

    def get_balance(self):
        """Not implemented yet"""
        pass

    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        """Not implemented yet"""
        pass

    def parse_tx(self, tx):
        return {
            'symbol': tx['code'],
            'date': dateutil.parser.parse(tx['timestamp']),
            'from_address': tx['sender'],
            'to_address': tx['receiver'],
            'amount': tx['quantity'],
            # 'fee': fee,
            # 'gas_used': int(tx['gas_used']),
            # 'gas_limit': int(tx['gas_wanted']),
            'hash': tx['trx_id'],
            # 'block_hash': None,
            # 'block_num': tx['block_num'],
            'confirmed': True,
            'is_error': False,
            'type': 'normal' if tx['symbol'] == 'EOS' else 'token',
            'kind': 'transaction',
            'direction': 'outgoing' if self.address == tx['sender'] else 'incoming',
            'raw': tx,
        }
