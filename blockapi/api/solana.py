import json

from blockapi.services import (
    APIError, BlockchainAPI,
)


class SolanaApi(BlockchainAPI):
    """
    Solana RPC
    API docs: https://docs.solana.com/apps/jsonrpc-api
    """

    symbol = 'SOL'
    base_url = 'https://api.mainnet-beta.solana.com/'
    rate_limit = None
    coef = 1e-9
    start_offset = 0
    max_items_per_page = 1000
    page_offset_step = 1

    # follow used pattern even though this API uses POST requests
    supported_requests = {
        'get_balance': '',
        'get_txs_signatures': '',
        'get_tx': ''
    }

    token_program_id = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'

    # mainnet tokens
    # https://github.com/solana-labs/explorer/blob/master/src/tokenRegistry.ts
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
        'AGFEad2et2ZJif9jaGpdMixQqvW5i81aBdvKe7PHNfz3': {
            'symbol': 'FTT',
            'name': 'Wrapped FTT',
        },
        '3JSf5tPeuscJGtaCp5giEiDhv51gQ4v3zWg8DGgyLfAB': {
            'symbol': 'YFI',
            'name': 'Wrapped YFI',
        },
        'CWE8jPTUYhdCTZYWPTe1o5DFqfdjzWKc9WKz6rSjQUdG': {
            'symbol': 'LINK',
            'name': 'Wrapped Chainlink',
        },
        'Ga2AXHpfAF6mv2ekZwcsJFqu7wB4NV331qNH7fW9Nst8': {
            'symbol': 'XRP',
            'name': 'Wrapped XRP',
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
        'AR1Mtgh7zAtxuxGd2XPovXPVjcSdY3i4rQYisNadjfKy': {
            'symbol': 'SUSHI',
            'name': 'Wrapped Sushi',
        },
        'SF3oTvfWzEP3DTwGSvUXRrGTvr75pdZNnBLAH9bzMuX': {
            'symbol': 'SXP',
            'name': 'Wrapped Swipe',
        },
        'CsZ5LZkDS7h9TDKjrbL7VAwQZ9nsRu8vJLhRYfmGaN8K': {
            'symbol': 'ALEPH',
            'name': 'Wrapped Aleph',
        },
    }

    def __init__(self, address, *args, **kwargs):
        super().__init__(address)
        self._headers = {
            'Content-Type': 'application/json'
        }

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
        response = self._request(
            method='getBalance',
            params=[self.address]
        )

        return {
            'symbol': self.symbol,
            'amount': response['result']['value'] * self.coef
        }

    def _get_token_balances(self):
        response = self._request(
            method='getTokenAccountsByOwner',
            params=[
                self.address,
                {
                    'programId': self.token_program_id
                },
                {
                    'encoding': 'jsonParsed'
                }
            ]
        )

        balances = [self._parse_token_balance(b)
                    for b in response['result']['value']]

        return balances

    def _parse_token_balance(self, raw):
        info = raw['account']['data']['parsed']['info']

        token_address = info['mint']
        token_info = self.tokens.get(token_address)

        _amount = info['tokenAmount']
        if _amount.get('uiAmount'):
            amount = _amount['uiAmount']
        elif _amount.get('decimals'):
            amount = float(_amount['amount']) * pow(10, -_amount['decimals'])
        else:
            amount = _amount['amount']

        return {
            'symbol': token_info['symbol'] if token_info else 'UNKNOWN',
            'address': token_address,
            'amount': amount,
            'name': token_info['name'] if token_info else 'Unknown',
            'account_address': raw['pubkey']
        }

    def get_txs_signatures(self, limit=None):
        if not limit:
            limit = self.max_items_per_page

        response = self._request(
            method='getConfirmedSignaturesForAddress2',
            params=[
                self.address,
                {
                    'limit': limit
                }
            ]
        )

        return [
            {
                'signature': r['signature'],
                'error': bool(r['err'])
            }
            for r in response['result']
        ]

    def get_tx(self, signature):
        response = self._request(
            method='getConfirmedTransaction',
            params=[
                signature,
                'jsonParsed'
            ]
        )
        return response['result']

    def _request(self, method, params):
        body = json.dumps({
            'jsonrpc': '2.0',
            'id': 1,
            'method': method,
            'params': params
        })

        response = self.request(
            # request method is not needed, it's included in body
            request_method=None,
            body=body,
            headers=self._headers
        )
        if response.get('error'):
            raise APIError(response['error'])

        return response
