from datetime import datetime

import pytz

from blockapi.services import APIError, BlockchainAPI


class AlethioAPI(BlockchainAPI):
    """
    Ethereum
    API docs: https://docs.aleth.io/api
    Explorer:
    notice: API key is needed
    """

    active = True

    symbol = 'ETH'
    base_url = 'https://api.aleth.io/v1'
    rate_limit = 1  # 1 req per second
    coef = 1e-18
    max_items_per_page = 100
    page_offset_step = None
    confirmed_num = None
    has_next = {'normal': True, 'token': True}
    collect_logs = True

    supported_requests = {
        'get_balance': '/accounts/{address}/etherBalances',
        'get_token_balances': '/accounts/{address}/tokenBalances',
        'get_token_info': '/tokens/{token_id}',
        'get_txs': '/transactions?filter[account]={address}&page[limit]={limit}'
        '&page[next]={page}',
        'get_txs_next': None,
        'get_token_txs': '/token-transfers?filter[account]={address}'
        '&page[limit]={limit}&page[next]={page}',
        'get_token_txs_next': None,
        'get_logs': None,
        'get_info': '/accounts/{address}',
    }

    def __init__(self, address, api_key=None):
        self.has_next['normal'] = True
        self.has_next['token'] = True
        self._address_type = None
        self.supported_requests['get_txs_next'] = None
        self.supported_requests['get_token_txs_next'] = None
        self.supported_requests['get_logs'] = None
        super().__init__(address, api_key)

    def _query_api(self, request_method, **kwargs):
        return self.request(
            request_method,
            headers={'Authorization': 'Bearer {}'.format(self.api_key)},
            **kwargs
        )

    def get_balance(self):
        """
        Returns a list of all balances, both Ethereum and token ones

        :return: list
        """
        response = self._query_api('get_balance', address=self.address)
        if not response:
            return None

        amount = int(response['data'][0]['attributes']['balance']) * self.coef
        balance_eth = [
            {'symbol': self.symbol, 'amount': amount, 'name': 'Ethereum', 'address': ''}
        ]
        balances_tokens = self._get_token_balances()
        if balances_tokens is None:
            return None

        return balance_eth + balances_tokens

    def _get_token_balances(self):
        response = self._query_api('get_token_balances', address=self.address)
        if not response:
            return None

        balances = []

        for token in response['data']:
            bal = token['attributes']['balance']
            if bal is None:
                continue

            token_id = token['relationships']['token']['data']['id']
            token_info = self._query_api('get_token_info', token_id=token_id)
            if not token_info:
                return None

            token_info_attrs = token_info['data']['attributes']
            token_decimals = int(token_info_attrs['decimals'])
            token_symbol = token_info_attrs['symbol']
            token_name = token_info_attrs['name']

            token_balance = int(bal) * pow(10, -token_decimals)

            balances.append(
                {
                    'address': token_id,
                    'name': token_name,
                    'symbol': token_symbol,
                    'amount': token_balance,
                }
            )

        return balances

    def get_txs(self, page=None, limit=None, unconfirmed=False, collect_logs=True):
        """
        Returns the list of collected transactions, subsequent calls
        download next transactions if available

        :param page: tx cursor
        :param limit: page limit; 100 is the maximum with AlethioAPI
        :param unconfirmed: not used at all here
        :param collect_logs: True if you'd like to collect eventlogs for each
                             transaction, otherwise False
        :return: list
        """
        self.collect_logs = collect_logs
        return self._get_txs(tx_type='normal', page=page, limit=limit)

    def get_token_txs(self, page=None, limit=None, unconfirmed=False):
        """
        Returns a list of collected token transactions, subsequent calls
        download next transactions if available

        :param page: tx cursor
        :param limit: page limit; 100 is the maximum with AlethioAPI
        :param unconfirmed: not used here at all
        :return: list
        """
        return self._get_txs(tx_type='token', page=page, limit=limit)

    def _get_txs(self, tx_type='normal', page=None, limit=None, unconfirmed=False):
        if tx_type == 'normal':
            fetch_req = 'get_txs'
            fetch_next_req = 'get_txs_next'
            parser = self._parse_tx
        else:
            fetch_req = 'get_token_txs'
            fetch_next_req = 'get_token_txs_next'
            parser = self._parse_token_tx

        if page is None:
            page = ''

        if not self.has_next[tx_type]:
            return []

        if limit is None:
            limit = self.max_items_per_page

        if limit > self.max_items_per_page:
            limit = self.max_items_per_page

        if self.supported_requests[fetch_next_req] is None:
            txs = self._query_api(
                fetch_req, address=self.address, page=page, limit=limit
            )
        else:
            txs = self._query_api(fetch_next_req)

        if txs['meta']['page']['hasNext']:
            self.has_next[tx_type] = True
            self.supported_requests[fetch_next_req] = txs['links']['next'].replace(
                self.base_url, ''
            )
        else:
            self.has_next[tx_type] = False

        parsed_txs = [parser(tx) for tx in txs['data']]
        return parsed_txs

    def _parse_token_tx(self, tx):
        attributes = tx['attributes']
        relationships = tx['relationships']

        tx_symbol = attributes['symbol']
        tx_from_address = relationships['from']['data']['id']
        tx_to_address = relationships['to']['data']['id']
        tx_contract_address = relationships['token']['data']['id']

        tx_direction = self._get_tx_direction(
            tx_from_address, tx_to_address, tx_contract_address
        )
        tx_token_data = {
            'name': None,  # there's no such field
            'symbol': tx_symbol,
            'decimals': attributes['decimals'],
        }

        return {
            'symbol': tx_symbol,
            'date': datetime.fromtimestamp(
                int(attributes['blockCreationTime']), pytz.utc
            ),
            'from_address': tx_from_address,
            'to_address': tx_to_address,
            'contract_address': tx_contract_address,
            'amount': float(attributes['value']) * pow(10, -attributes['decimals']),
            'fee': 0.0,
            'gas': {
                'gas': float(attributes['transactionGasLimit']),
                'gas_price': float(attributes['transactionGasPrice']),
                'cumulative_gas_used': None,
                'gas_used': float(attributes['transactionGasUsed']),
            },
            'hash': relationships['transaction']['data']['id'],
            'confirmations': None,
            'confirmed': None,
            'is_error': False,  # should be always valid
            'type': 'token',
            'kind': 'transaction',
            'direction': tx_direction,
            'token_data': tx_token_data,
            'page': attributes['cursor'],
            'raw': tx,
        }

    def _parse_tx(self, tx):
        attributes = tx['attributes']
        relationships = tx['relationships']

        tx_from_address = relationships['from']['data']['id']
        tx_to_address = relationships['to']['data']['id']
        if attributes['msgType'] in ('CallTx', 'CreateTx'):
            tx_contract_address = tx_to_address
        else:
            tx_contract_address = ''

        tx_direction = self._get_tx_direction(
            tx_from_address, tx_to_address, tx_contract_address
        )
        log_entries_req = relationships['logEntries']['links']['related']
        self.supported_requests['get_logs'] = log_entries_req.replace(self.base_url, '')

        if self.collect_logs:
            parsed_logs = self._get_logs()
        else:
            parsed_logs = None

        return {
            'symbol': 'ETH',
            'date': datetime.fromtimestamp(
                int(attributes['blockCreationTime']), pytz.utc
            ),
            'from_address': tx_from_address,
            'to_address': tx_to_address,
            'contract_address': tx_contract_address,
            'amount': float(attributes['value']) * self.coef,
            'fee': float(attributes['fee']) * self.coef,
            'gas': {
                'gas': float(attributes['msgGasLimit']),
                'gas_price': float(attributes['txGasPrice']),
                'cumulative_gas_used': None,
                'gas_used': float(attributes['txGasUsed']),
            },
            'hash': attributes['txHash'],
            'confirmations': None,
            'confirmed': None,
            'is_error': attributes['msgError'],
            'type': 'normal',
            'kind': 'transaction',
            'direction': tx_direction,
            'token_data': None,
            'page': attributes['cursor'],
            'raw': tx,
            'event_logs': parsed_logs,
        }

    def _get_tx_direction(self, tx_from_address, tx_to_address, tx_contract_address):
        tx_direction = None
        if self.address.lower() == tx_from_address.lower():
            tx_direction = 'outgoing'
        elif self.address.lower() == tx_to_address.lower():
            tx_direction = 'incoming'
        elif not tx_contract_address:
            tx_direction = 'outgoing'

        return tx_direction

    def _get_logs(self):
        response = self._query_api('get_logs')
        if not response:
            return None

        logs = []

        next_logs = True
        while next_logs:
            for log in response['data']:
                logs.append(self._parse_log(log))
            next_logs = response['meta']['page']['hasNext']
            if next_logs:
                self.supported_requests['get_logs'] = response['links']['next'].replace(
                    self.base_url, ''
                )
                response = self._query_api('get_logs')

        return logs

    def _parse_log(self, log):
        attributes = log['attributes']
        relationships = log['relationships']

        if attributes['eventDecodedError'] == '':
            event_name = attributes['eventDecoded']['event']
            inputs = self._parse_log_inputs(attributes)
        else:
            event_name = ''
            inputs = None

        result = {
            'log_data': attributes['logData'],
            'event': event_name,
            'inputs': inputs,
            'address': relationships['loggedBy']['data']['id'],
        }

        topics = attributes['hasLogTopics']

        i = 0
        for topic in topics:
            result['topic{}'.format(i)] = topic
            i += 1

        return result

    def _parse_log_inputs(self, attributes):
        inputs = []
        if 'inputs' in attributes['eventDecoded']:
            for inp in attributes['eventDecoded']['inputs']:
                if 'indexed' in inp:
                    is_indexed = inp['indexed']
                else:
                    is_indexed = False

                parsed_log = {
                    'name': inp['name'],
                    'type': inp['type'],
                    'is_indexed': is_indexed,
                }
                if 'value' in inp:
                    parsed_log['value'] = inp['value']
                if 'components' in inp:
                    parsed_log['components'] = inp['components']

                inputs.append(parsed_log)

        return inputs

    @property
    def address_type(self):
        if self._address_type is None:
            result = self._query_api('get_info', address=self.address)
            if result['data']['relationships']['contract']['data'] is None:
                self._address_type = 'address'
            else:
                # contract or token
                try:
                    self._query_api('get_token_info', token_id=self.address)
                    self._address_type = 'token'
                except APIError:
                    self._address_type = 'contract'

        return self._address_type
