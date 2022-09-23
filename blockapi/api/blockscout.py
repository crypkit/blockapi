from blockapi.services import BlockchainAPI


class BlockscoutAPI(BlockchainAPI):
    """
    Multi coins: ethereum classic, xDAI, POA
    API docs: https://blockscout.com/{chain}/{network}/api_docs
    Explorer: https://blockscout.com
    """

    active = True

    rate_limit = 0
    coef = 1e-18
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'eth_get_balance': '?module=account&action=eth_get_balance'
        '&address={address}',
        'get_balance': '?module=account&action=balance&address={address}',
        'get_token_list': '?module=account&action=tokenlist&address={address}',
        'get_token_balance': '?module=account&action=tokenbalance'
        '&contractaddress={contract}&address={address}',
    }

    def eth_get_balance(self):
        response = self.request('eth_get_balance', address=self.address)
        if not response:
            return []

        amount = int(response['result'], 16) * self.coef
        return [{'symbol': self.symbol, 'amount': amount}]

    def get_balance(self):
        balances = []

        main_balance = self._get_main_balance()
        if main_balance:
            balances.append(main_balance)

        token_balances = self._get_token_balances()
        if token_balances:
            balances += token_balances

        return balances

    def _get_main_balance(self):
        response = self.request('get_balance', address=self.address)
        if response['message'] != 'OK':
            return

        return {'symbol': self.symbol, 'amount': int(response['result']) * self.coef}

    def _get_token_balances(self):
        response = self.request('get_token_list', address=self.address)
        if response['message'] != 'OK':
            return

        return [
            self._parse_token_balance(t)
            for t in response['result']
            if int(t['balance'])
        ]

    @staticmethod
    def _parse_token_balance(raw):
        decimals = int(raw.get('decimals', 0))

        return {
            'symbol': raw.get('symbol', 'UNKNOWN'),
            'address': raw['contractAddress'],
            'amount': (
                float(raw['balance']) * pow(10, -decimals)
                if decimals
                else float(raw['amount'])
            ),
            'name': raw.get('name', 'Unknown'),
            'type': raw.get('type', 'UNKNOWN'),
            'decimals': decimals,
        }


class BlockscoutEthereumClassicAPI(BlockscoutAPI):
    """
    xDAI
    API docs: https://blockscout.com/etc/mainnet/api
    Explorer: https://blockscout.com/etc/mainnet
    """

    symbol = 'ETC'
    base_url = 'https://blockscout.com/etc/mainnet/api'


class BlockscoutXdaiAPI(BlockscoutAPI):
    """
    xDAI
    API docs: https://blockscout.com/poa/xdai/api
    Explorer: https://blockscout.com/poa/xdai
    """

    symbol = 'STAKE'
    base_url = 'https://blockscout.com/poa/xdai/api'
