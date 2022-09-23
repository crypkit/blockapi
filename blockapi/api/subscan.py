import json
from datetime import datetime
from decimal import Decimal

from blockapi.services import AddressNotExist, APIError, BlockchainAPI
from blockapi.utils.num import to_decimal


class SubscanAPI(BlockchainAPI):
    """
    API docs: https://docs.api.subscan.io/
    Explorer: https://www.subscan.io
    """

    api_url = 'api.subscan.io'
    rate_limit = 0
    coef = Decimal('1e-12')
    max_items_per_page = 50
    page_offset_step = 1
    confirmed_num = None
    xpub_support = True

    supported_requests = {
        'get_balance': '/api/v2/scan/search',
        'get_txs': '/api/scan/transfers',
        'get_rewards': '/api/scan/account/reward_slash',
        'get_staking': '/api/v2/scan/search',
    }

    def __init__(self, address, api_key=None, *args, **kwargs):
        super().__init__(address, api_key)
        self._headers = {'Content-Type': 'application/json'}

    def get_balance(self):
        body = json.dumps(
            {
                'key': self.address,
                'row': 1,
                'page': 0,
            }
        )

        response = self.request(
            'get_balance', body=body, headers=self._headers, api_key=self.api_key
        )

        if response['code'] == 0:
            return [
                {
                    'symbol': self.symbol,
                    'amount': to_decimal(response['data']['account']['balance']),
                }
            ]
        elif response['code'] == 10004:
            raise AddressNotExist()
        else:
            raise APIError(response['message'])

    def get_txs(self, offset=0, limit=10, unconfirmed=False):
        body = json.dumps({'address': self.address, 'page': offset, 'row': limit})

        response = self.request(
            'get_txs', body=body, headers=self._headers, api_key=self.api_key
        )

        if response['code'] == 0:
            transfers = (self._parse_tx(t) for t in response['data']['transfers'])
            return [t for t in transfers if unconfirmed or t['confirmed']]
        elif response['code'] == 10004:
            raise AddressNotExist()
        else:
            raise APIError(response['message'])

    def _parse_tx(self, tx):
        if tx['from'] == self.address:
            direction = 'outgoing'
        else:
            direction = 'incoming'

        return {
            'date': datetime.fromtimestamp(tx['block_timestamp']),
            'from_address': tx['from'],
            'to_address': tx['to'],
            'amount': to_decimal(tx['amount']),
            'fee': to_decimal(tx['fee']) * self.coef,
            'hash': tx['hash'],
            'confirmed': tx['success'],
            'is_error': not tx['success'],
            'type': 'normal',
            'kind': 'transaction',
            'direction': direction,
            'raw': tx,
        }

    def get_rewards(self, offset=0, limit=20):
        body = json.dumps({'address': self.address, 'row': limit, 'page': offset})

        response = self.request(
            'get_rewards', body=body, headers=self._headers, api_key=self.api_key
        )

        if response['code'] == 0:
            return [
                self._parse_reward(r)
                for r in (
                    response['data']['list']
                    if response['data']['list'] is not None
                    else []
                )
            ]
        elif response['code'] == 10004:
            raise AddressNotExist()
        else:
            raise APIError(response['message'])

    def _parse_reward(self, reward):
        if reward['event_id'] == 'Reward':
            sign = 1
        else:
            sign = -1

        return {
            'amount': to_decimal(reward['amount']) * self.coef * sign,
            'hash': reward['extrinsic_hash'],
            'event_index': reward['event_index'],
        }

    def get_staking(self, offset=0, limit=20):
        body = json.dumps({'key': self.address, 'row': limit, 'page': offset})

        response = self.request(
            'get_staking', body=body, headers=self._headers, api_key=self.api_key
        )

        if response['code'] == 0:
            return to_decimal(response['data']['account']['balance_lock'])
        elif response['code'] == 10004:
            raise AddressNotExist()
        else:
            raise APIError(response['message'])


class SubscanPolkaAPI(SubscanAPI):
    chain_name = 'polkadot'
    symbol = 'DOT'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanKusamaAPI(SubscanAPI):
    chain_name = 'kusama'
    symbol = 'KSM'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanDarwiniaAPI(SubscanAPI):
    chain_name = 'darwinia'
    symbol = 'RING'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanDarwiniaCrabAPI(SubscanAPI):
    chain_name = 'crab'
    symbol = 'CRING'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanChainXAPI(SubscanAPI):
    chain_name = 'chainx'
    symbol = 'PCX'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanCloverAPI(SubscanAPI):
    chain_name = 'clover'
    symbol = 'CLV'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanEdgewareAPI(SubscanAPI):
    chain_name = 'edgeware'
    symbol = 'EDG'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanCentrifugeAPI(SubscanAPI):
    chain_name = 'centrifuge'
    symbol = 'CFG'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanPlasmAPI(SubscanAPI):
    chain_name = 'plasm'
    symbol = 'PLM'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanDockAPI(SubscanAPI):
    chain_name = 'dock'
    symbol = 'DCK'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanKulupuAPI(SubscanAPI):
    chain_name = 'kulupu'
    symbol = 'KLP'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanStafiAPI(SubscanAPI):
    chain_name = 'stafi'
    symbol = 'FIS'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanDataHighwayAPI(SubscanAPI):
    chain_name = 'datahighway'
    symbol = 'DHX'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanEquilibriumAPI(SubscanAPI):
    chain_name = 'equilibrium'
    symbol = 'EQ'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanRococoV1API(SubscanAPI):
    chain_name = 'rococo'
    symbol = 'ROC'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanWestendAPI(SubscanAPI):
    chain_name = 'westend'
    symbol = 'WND'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanMoonbaseAPI(SubscanAPI):
    chain_name = 'moonbase'
    symbol = 'DEV'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanCloverTestnetAPI(SubscanAPI):
    chain_name = 'clover-testnet'
    symbol = 'CLV'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanGatewayAPI(SubscanAPI):
    chain_name = 'gateway-testnet'
    symbol = 'CASH'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanAcalaMandalaAPI(SubscanAPI):
    chain_name = 'acala-testnet'
    symbol = 'ACA'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanPhalaVendettaAPI(SubscanAPI):
    chain_name = 'phala'
    symbol = 'tPHA'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanCrustMaxwellAPI(SubscanAPI):
    chain_name = 'crust'
    symbol = 'CRU'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanDataHighwayHarbourAPI(SubscanAPI):
    chain_name = 'datahighway-harbour'
    symbol = 'DHX'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'


class SubscanPangolinAPI(SubscanAPI):
    chain_name = 'pangolin'
    symbol = 'PRING'
    base_url = f'https://{chain_name}.{SubscanAPI.api_url}'
