from blockapi.services import BlockchainAPI


class OntioAPI(BlockchainAPI):
    """
    coins: ontology
    API docs: https://docs.ont.io/developer-tools/api/explorer-api
    Explorer: https://explorer.ont.io
    """

    active = True

    symbol = 'ONT'
    base_url = 'https://explorer.ont.io'
    rate_limit = 0
    coef = 1
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {'get_balance': '/v2/addresses/{address}/all/balances'}

    def get_balance(self):
        response = self.request('get_balance', address=self.address)
        if not response or response['msg'] != 'SUCCESS':
            return []

        balances = []
        for r in response['result']:
            # what about 'waitboundong' and 'unboundong'?
            if r['asset_name'] in ['ont', 'ong']:
                balances.append(
                    {'symbol': r['asset_name'].upper(), 'amount': float(r['balance'])}
                )
        return balances
