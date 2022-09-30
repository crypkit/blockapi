import json
from decimal import Decimal

from blockapi.services import APIError, BlockchainAPI
from blockapi.utils.num import to_decimal


class SolanaApi(BlockchainAPI):
    """
    Solana RPC
    API docs: https://docs.solana.com/apps/jsonrpc-api
    """

    symbol = 'SOL'
    base_url = 'https://api.mainnet-beta.solana.com/'
    rate_limit = None
    coef = Decimal('1e-9')
    start_offset = 0
    max_items_per_page = 1000
    page_offset_step = 1

    # follow used pattern even though this API uses POST requests
    supported_requests = {'get_balance': '', 'get_txs_signatures': '', 'get_tx': ''}

    token_program_id = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'

    # mainnet tokens
    # https://github.com/solana-labs/token-list/blob/main/src/tokens/solana.tokenlist.json
    tokens = {
        'SRMuApVNdxXokk5GT7XD5cUUgXMBCoAz2LHeuAoKWRt': {
            'name': 'Serum',
            'symbol': 'SRM',
        },
        'MSRMcoVyrFxnSgo5uXwone5SKcGhT1KEJMFEkMEWf9L': {
            'name': 'MegaSerum',
            'symbol': 'MSRM',
        },
        '9n4nbM75f5Ui33ZbPYXn59EwSgE8CGsHtAeTH5YFeJ9E': {
            'symbol': 'BTC',
            'name': 'Wrapped Bitcoin',
        },
        '2FPyTwcZLUg1MDrwsyoP4D6s1tM7hAkHYRjkNb5w6Pxk': {
            'symbol': 'ETH',
            'name': 'Wrapped Ethereum',
        },
        'BQcdHdAQW1hczDbBi9hiegXAR7A98Q9jx3X3iBBBDiq4': {
            'symbol': 'USDT',
            'name': 'Wrapped USDT',
        },
        'BXXkv6z8ykpG1yuvUDPgh732wzVHB69RnB9YgSYh3itW': {
            'symbol': 'USDC',
            'name': 'Wrapped USDC',
        },
        'So11111111111111111111111111111111111111112': {
            'symbol': 'SOL',
            'name': 'Wrapped SOL',
        },
    }

    def __init__(self, address, *args, **kwargs):
        super().__init__(address)
        self._headers = {'Content-Type': 'application/json'}

    def get_balance(self):
        balances = []

        sol_balance = self._get_sol_balance()
        if sol_balance:
            balances.append(sol_balance)

        token_balances = self._get_token_balances()
        if token_balances:
            balances += token_balances

        return balances

    def _get_sol_balance(self):
        response = self._request(method='getBalance', params=[self.address])

        return {
            'symbol': self.symbol,
            'amount': to_decimal(response['result']['value']) * self.coef,
        }

    def _get_token_balances(self):
        response = self._request(
            method='getTokenAccountsByOwner',
            params=[
                self.address,
                {'programId': self.token_program_id},
                {'encoding': 'jsonParsed'},
            ],
        )

        balances = [self._parse_token_balance(b) for b in response['result']['value']]

        return [b for b in balances if b['amount'] > Decimal(0)]

    def _parse_token_balance(self, raw):
        info = raw['account']['data']['parsed']['info']

        token_address = info['mint']
        token_info = self.tokens.get(token_address)

        a = info['tokenAmount']
        if a.get('uiAmount'):
            amount = to_decimal(a['uiAmount'])
        elif a.get('decimals'):
            amount = to_decimal(a['amount']) * Decimal(f"10e-{a['decimals']}")
        else:
            amount = to_decimal(a['amount'])

        return {
            'symbol': token_info['symbol'] if token_info else 'UNKNOWN',
            'address': token_address,
            'amount': amount,
            'name': token_info['name'] if token_info else 'Unknown',
            'account_address': raw['pubkey'],
        }

    def get_txs_signatures(self, limit=None):
        if not limit:
            limit = self.max_items_per_page

        response = self._request(
            method='getConfirmedSignaturesForAddress2',
            params=[self.address, {'limit': limit}],
        )

        return [
            {'signature': r['signature'], 'error': bool(r['err'])}
            for r in response['result']
        ]

    def get_tx(self, signature):
        response = self._request(
            method='getConfirmedTransaction', params=[signature, 'jsonParsed']
        )
        return response['result']

    def _request(self, method, params):
        body = json.dumps(
            {'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}
        )

        response = self.request(
            # request method is not needed, it's included in body
            request_method=None,
            body=body,
            headers=self._headers,
        )
        if response.get('error'):
            raise APIError(response['error'])

        return response
