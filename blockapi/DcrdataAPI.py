import pytz
from datetime import datetime
from .services import BlockchainAPI,set_default_args_values,APIError,AddressNotExist,BadGateway,GatewayTimeOut

class DcrdataAPI(BlockchainAPI):
    """
    Decred
    API docs: https://github.com/decred/dcrdata#dcrdata-api
    Explorer: https://explorer.dcrdata.org
    """

    currency_id = 'decred'
    base_url = 'https://explorer.dcrdata.org/api'
    rate_limit = 0
    coef = 1
    max_items_per_page = 50000
    page_offset_step = max_items_per_page
    confirmed_num = 60

    supported_requests = {
        'get_balance': '/address/{address}/totals',
        'get_transaction': '/tx/{tx_hash}?spends=true',
        'get_txs': '/address/{address}/count/{count}/skip/{skip}/raw'
    }

    def process_error_response(self, response):
        if response.status_code == 422:
            raise AddressNotExist()
        # else
        super().process_error_response(response)

    def get_balance(self):
        balance = self.request('get_balance', address=self.address)
        return balance['dcr_unspent']
    
    @set_default_args_values
    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        txs = self.request(
            'get_txs',
            address=self.address,
            count=limit,
            skip=offset
        )
        
        parsed_txs = []
        for tx in txs:
            parsed_txs += self.parse_tx(tx)
        
        return BlockchainAPI.filter_unconfirmed_txs(parsed_txs)
    
    def get_tx(self, tx_hash):
        tx = self.request('get_transaction', tx_hash=tx_hash)
        for parsed in self.parse_tx(tx):
            return parsed[0]
        return None

    def parse_tx(self, tx):
        # TX in decred could contain several addresses, filter only mine
        ins = [v for v in tx['vin']
            if self.address in v.get('prevOut', {}).get('addresses', [])]
        outs = [o for o in tx['vout']
            if self.address in o.get('scriptPubKey', {}).get('addresses', [])]
        
        date = datetime.fromtimestamp(tx['time'], pytz.utc)
        kind = self._get_tx_kind(tx)
        status = self._get_tx_status(tx)

        parsed = []
        for i in ins:
            parsed.append({
                'date': date,
                'from_address': self.address,
                'to_address': None, # multiple, TODO check it
                'amount': i['amountin'],
                'fee': None,
                'gas_limit': None,
                'hash': tx['txid'],
                'confirmed': tx['confirmations'] > self.confirmed_num,
                'is_error': False,
                'type': 'normal',
                'kind': kind,
                'direction': 'outgoing',
                'status': status,
                'raw': tx
            })

        for o in outs:
            parsed.append({
                'date': date,
                'from_address': None,  # multiple, TODO check it
                'to_address': self.address,
                'amount': o['value'],
                'fee': None,
                'gas_limit': None,
                'hash': tx['txid'],
                'confirmed': tx['confirmations'] > self.confirmed_num,
                'is_error': False,
                'type': 'normal',
                'kind': kind,
                'direction': 'incoming',
                'status': status,
                'raw': tx
            })
        return parsed
    
    def _get_tx_kind(self, tx):
        tx_types = [t['scriptPubKey']['type'] for t in tx['vout']]
        if 'stakesubmission' in tx_types:  # and 'sstxcommitment', 'sstxchange'
            return 'ticket'
        elif 'stakegen' in tx_types:  # and 'nulldata'
            return 'vote'
        elif 'stakerevoke' in tx_types:
            return 'revocation'
        elif 'pubkeyhash' in tx_types:
            return 'transaction' #  'regular' in api
        return None
    
    def _get_tx_status(self, tx):
        status = None

        # only for ticket
        if self._get_tx_kind(tx) == 'ticket':
            voted = next((True for t in tx['vout']
                if t['scriptPubKey']['type'] == 'stakesubmission'
                and t.get('spend')), False)
            if voted:
                status = 'voted'
            elif tx['confirmations'] < 256:
                status = 'immature'
            else:
                status = 'live'
        
        return status
    

