from blockapi.services import BlockchainAPI


class AmberdataAPI(BlockchainAPI):
    """
    Ethereum
    API docs: https://docs.amberdata.io/reference#get-all-addresses
    """

    symbol = 'ETH'
    base_url = 'https://web3api.io/api/v2'
    # 3 reqs per second with free api key, but doesn't work well
    rate_limit = 2
    coef = 1e-18
    start_offset = 0
    max_items_per_page = 100
    page_offset_step = 1

    supported_requests = {
        'get_balance': '/addresses/{address}/account-balances/latest',
        'get_token_balance': '/addresses/{address}/tokens?page={page}&size={size}',
        'get_token_info': '/addresses/{address}/information?include_price={include_price}',
    }

    def __init__(self, address, api_key):
        super().__init__(address, api_key)
        self._headers = {
            'x-amberdata-blockchain-id': 'ethereum-mainnet',
            'x-api-key': self.api_key,
        }

    def get_balance(self):
        balances = []

        eth_balance = self._get_eth_balance()
        if eth_balance:
            balances.append(eth_balance)

        token_balances = self._get_token_balances()
        if token_balances:
            balances += token_balances

        return balances

    def _get_eth_balance(self):
        response = self.request(
            'get_balance', address=self.address, headers=self._headers
        )
        if response['status'] != 200:
            return

        return {
            'symbol': 'ETH',
            'amount': int(response['payload']['value']) * self.coef,
        }

    def _get_token_balances(self):
        balances = []
        page = self.start_offset

        while True:
            response = self.request(
                'get_token_balance',
                address=self.address,
                page=page,
                size=self.max_items_per_page,
                headers=self._headers,
            )
            if response['status'] != 200:
                break

            balances += [
                self._parse_token_balance(b) for b in response['payload']['records']
            ]

            if len(balances) == int(response['payload']['totalRecords']):
                break

            page += self.page_offset_step

        return balances

    @staticmethod
    def _parse_token_balance(raw):
        decimals = int(raw.get('decimals'))

        if raw['isERC20']:
            type_ = 'ERC-20'

            # TODO ignore coin if decimals = 0, it's okay?
            if decimals == 0:
                decimals = None
        elif raw['isERC721']:
            type_ = 'ERC-721'
        elif raw['isERC777']:
            type_ = 'ERC-777'
        elif raw['isERC884']:
            type_ = 'ERC-884'
        elif raw['isERC998']:
            type_ = 'ERC-998'
        else:
            type_ = None

        return {
            'symbol': raw.get('symbol', 'UNKNOWN'),
            'address': raw['address'],
            'amount': (
                float(raw['amount']) * pow(10, -decimals) if decimals is not None else 0
            ),
            'name': raw.get('name', 'Unknown'),
            'type': type_,
        }

    @classmethod
    def get_token_info(cls, token_address, api_key, include_price=False):
        api = cls(token_address, api_key)
        response = api.request(
            'get_token_info',
            address=token_address,
            include_price=include_price,
            api_key=api.api_key,
            headers=api._headers,
        )
        if response['status'] != 200:
            return

        if response.get('payload'):
            return api._parse_token_info(token_address, response['payload'])

    @staticmethod
    def _parse_token_info(token_address, raw):
        symbol = raw['symbol'] if raw.get('symbol') else 'UNKNOWN'
        name = raw['name'] if raw.get('name') else 'Unknown'

        d = raw.get('decimals')
        decimals = int(d) if d else 0

        contract_types = raw.get('contractTypes', [])
        if 'Token' in contract_types or 'ERC20' in contract_types:
            type_ = 'ERC-20'
        elif 'ERC721' in contract_types:
            type_ = 'ERC-721'
        else:
            type_ = contract_types[0] if contract_types else 'Unknown'

        return {
            'symbol': symbol,
            'address': token_address,
            'name': name,
            'decimals': decimals,
            'type': type_,
        }
