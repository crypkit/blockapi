from datetime import datetime
import pytz

from blockapi.services import (
    BlockchainAPI
)


class OntioAPI(BlockchainAPI):
    """
    coins: ontology
    API docs: https://dev-docs.ont.io/#/docs-en/API/02-restful_api
              https://github.com/ontio/ontology-explorer/tree/master/back-end-projects/Explorer/src/main/java/com/github/ontio/controller
    Explorer: https://explorer.ont.io
    """

    active = True

    symbol = 'ONT'
    base_url = 'https://explorer.ont.io'
    rate_limit = 0
    coef = 1
    max_items_per_page = 20
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': '/api/v1/explorer/address/{address}/0/1',
        'get_txs': '/api/v1/explorer/address/{address}/{limit}/{page}'
    }

    def get_balance(self):
        response = self.request('get_balance',
                                address=self.address)
        if not response:
            return 0

        return [{"symbol": item['AssetName'], "amount": item['Balance']} for item in response['Result']['AssetBalance']]


    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        if limit is None:
            limit = self.max_items_per_page
        if offset is None:
            offset = 1

        response = self.request('get_txs',
                                address=self.address,
                                limit=limit,
                                page=offset)

        txs = response['Result']['TxnList']

        txs_result = []

        for tx in txs:
            for tx_transfer in tx['TransferList']:
                txs_result.append({
                    'date': datetime.fromtimestamp(tx['TxnTime'], pytz.utc),
                    'from_address': tx_transfer['FromAddress'],
                    'to_address': tx_transfer['ToAddress'],
                    'amount': tx_transfer['Amount'] * self.coef,
                    'fee': tx['Fee'] * self.coef,
                    'hash': tx['TxnHash'],
                    'confirmed': None,
                    'is_error': False,
                    'type': 'normal',
                    'kind': 'transaction',
                    'direction': 'outgoing' if tx_transfer['FromAddress'] == self.address else 'incoming',
                    'status': 'confirmed' if tx['ConfirmFlag'] == 1 else 'unconfirmed',
                    'raw': tx
                })


        return txs_result
