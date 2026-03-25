from decimal import Decimal

import pytest

from blockapi.v2.api.terra import TerraApi
from blockapi.v2.models import AssetType, Blockchain


@pytest.fixture()
def terra_api(requests_mock):
    """TerraApi with token mapping disabled to avoid external calls."""
    requests_mock.get(
        'https://raw.githubusercontent.com/PulsarDefi/IBC-Token-Data-Cosmos/main/native_token_data.min.json',
        json={
            'uluna__terra': {
                'name': 'Terra Classic',
                'chain': 'terra',
                'denom': 'uluna',
                'symbol': 'LUNC',
                'decimals': 6,
                'coingecko_id': 'terra-luna',
                'bridge_asset': None,
                'logos': {},
            },
        },
    )
    requests_mock.get(
        'https://raw.githubusercontent.com/PulsarDefi/IBC-Token-Data-Cosmos/main/ibc_data.min.json',
        json={},
    )
    return TerraApi()


@pytest.fixture()
def balances_response():
    return {
        'balances': [
            {'denom': 'uluna', 'amount': '23068009633'},
            {'denom': 'uusd', 'amount': '85997844'},
        ],
        'pagination': {'next_key': None, 'total': '2'},
    }


@pytest.fixture()
def staking_response():
    return {
        'delegation_responses': [
            {
                'delegation': {
                    'delegator_address': 'terra1test',
                    'validator_address': 'terravaloper1test',
                    'shares': '100000000.000000000000000000',
                },
                'balance': {'denom': 'uluna', 'amount': '100000000'},
            }
        ],
        'pagination': {'next_key': None, 'total': '1'},
    }


@pytest.fixture()
def unbonding_response():
    return {
        'unbonding_responses': [],
        'pagination': {'next_key': None, 'total': '0'},
    }


@pytest.fixture()
def rewards_response():
    return {
        'rewards': [
            {
                'validator_address': 'terravaloper1test',
                'reward': [
                    {'denom': 'uluna', 'amount': '5000000.000000000000000000'},
                    {'denom': 'uusd', 'amount': '1000000.000000000000000000'},
                ],
            }
        ],
        'total': [
            {'denom': 'uluna', 'amount': '5000000.000000000000000000'},
            {'denom': 'uusd', 'amount': '1000000.000000000000000000'},
        ],
    }


@pytest.fixture()
def ibc_denom_trace_response():
    return {
        'denom_trace': {
            'path': 'transfer/channel-7',
            'base_denom': 'xrowan',
        }
    }


ADDRESS = 'terra1yltenl48mhl370ldpyt83werd9x3s645509gaf'
BASE_URL = 'https://terra-classic-fcd.publicnode.com'


def test_terra_api_options():
    api = TerraApi(enable_token_mapping=False)
    assert api.api_options.blockchain == Blockchain.TERRA
    assert api.coin.symbol == 'LUNC'
    assert api.TOKENS_MAP_BLOCKCHAIN_KEY == 'terra'


def test_get_available_balances(terra_api, balances_response, requests_mock):
    requests_mock.get(
        f'{BASE_URL}/cosmos/bank/v1beta1/balances/{ADDRESS}',
        json=balances_response,
    )
    requests_mock.get(
        f'{BASE_URL}/cosmos/staking/v1beta1/delegations/{ADDRESS}',
        json={'delegation_responses': [], 'pagination': {}},
    )
    requests_mock.get(
        f'{BASE_URL}/cosmos/staking/v1beta1/delegators/{ADDRESS}/unbonding_delegations',
        json={'unbonding_responses': [], 'pagination': {}},
    )
    requests_mock.get(
        f'{BASE_URL}/cosmos/distribution/v1beta1/delegators/{ADDRESS}/rewards',
        json={'rewards': [], 'total': []},
    )

    balances = terra_api.get_balance(ADDRESS)

    available = [b for b in balances if b.asset_type == AssetType.AVAILABLE]
    assert len(available) == 2

    luna = next(b for b in available if b.coin.symbol == 'LUNC')
    assert luna.balance == Decimal('23068.009633')

    usd = next(b for b in available if b.coin.address == 'uusd')
    assert usd.balance == Decimal('85.997844')


def test_get_staking_balances(
    terra_api,
    balances_response,
    staking_response,
    unbonding_response,
    rewards_response,
    requests_mock,
):
    requests_mock.get(
        f'{BASE_URL}/cosmos/bank/v1beta1/balances/{ADDRESS}',
        json=balances_response,
    )
    requests_mock.get(
        f'{BASE_URL}/cosmos/staking/v1beta1/delegations/{ADDRESS}',
        json=staking_response,
    )
    requests_mock.get(
        f'{BASE_URL}/cosmos/staking/v1beta1/delegators/{ADDRESS}/unbonding_delegations',
        json=unbonding_response,
    )
    requests_mock.get(
        f'{BASE_URL}/cosmos/distribution/v1beta1/delegators/{ADDRESS}/rewards',
        json=rewards_response,
    )

    balances = terra_api.get_balance(ADDRESS)

    staked = [b for b in balances if b.asset_type == AssetType.STAKED]
    assert len(staked) == 1
    assert staked[0].balance == Decimal('100')
    assert staked[0].coin.symbol == 'LUNC'

    rewards = [b for b in balances if b.asset_type == AssetType.REWARDS]
    assert len(rewards) == 2

    luna_reward = next(b for b in rewards if b.coin.address == 'uluna')
    assert luna_reward.balance == Decimal('5')


def test_resolve_ibc_denom(terra_api, ibc_denom_trace_response, requests_mock):
    ibc_hash = '0A866A7A214C42CEF84430C8A4C7210C8C7A980548A9B9BE64316D1610A87C6C'
    ibc_denom = f'ibc/{ibc_hash}'

    requests_mock.get(
        f'{BASE_URL}/ibc/apps/transfer/v1/denom_traces/{ibc_hash}',
        json=ibc_denom_trace_response,
    )

    coin = terra_api.create_default_coin(ibc_denom)
    assert coin.symbol == 'ROWAN'
    assert coin.address == ibc_denom
    assert 'ibc' in coin.standards


def test_resolve_ibc_denom_fallback_on_error(terra_api, requests_mock):
    ibc_hash = 'DEADBEEF'
    ibc_denom = f'ibc/{ibc_hash}'

    requests_mock.get(
        f'{BASE_URL}/ibc/apps/transfer/v1/denom_traces/{ibc_hash}',
        status_code=404,
    )

    coin = terra_api.create_default_coin(ibc_denom)
    assert coin.address == ibc_denom
    assert coin.blockchain == Blockchain.TERRA


def test_non_ibc_denom_uses_default(terra_api):
    coin = terra_api.create_default_coin('ufoo')
    assert coin.address == 'ufoo'
    assert coin.blockchain == Blockchain.TERRA
    assert coin.decimals == 6


def test_get_balance_with_ibc_tokens(
    terra_api,
    staking_response,
    unbonding_response,
    rewards_response,
    ibc_denom_trace_response,
    requests_mock,
):
    ibc_hash = '0A866A7A214C42CEF84430C8A4C7210C8C7A980548A9B9BE64316D1610A87C6C'

    requests_mock.get(
        f'{BASE_URL}/cosmos/bank/v1beta1/balances/{ADDRESS}',
        json={
            'balances': [
                {'denom': 'uluna', 'amount': '1000000'},
                {'denom': f'ibc/{ibc_hash}', 'amount': '500000'},
            ],
            'pagination': {'next_key': None, 'total': '2'},
        },
    )
    requests_mock.get(
        f'{BASE_URL}/cosmos/staking/v1beta1/delegations/{ADDRESS}',
        json={'delegation_responses': [], 'pagination': {}},
    )
    requests_mock.get(
        f'{BASE_URL}/cosmos/staking/v1beta1/delegators/{ADDRESS}/unbonding_delegations',
        json={'unbonding_responses': [], 'pagination': {}},
    )
    requests_mock.get(
        f'{BASE_URL}/cosmos/distribution/v1beta1/delegators/{ADDRESS}/rewards',
        json={'rewards': [], 'total': []},
    )
    requests_mock.get(
        f'{BASE_URL}/ibc/apps/transfer/v1/denom_traces/{ibc_hash}',
        json=ibc_denom_trace_response,
    )

    balances = terra_api.get_balance(ADDRESS)
    assert len(balances) == 2

    rowan = next(b for b in balances if b.coin.symbol == 'ROWAN')
    assert rowan.balance == Decimal('0.5')
    assert 'ibc' in rowan.coin.standards


def test_unbonding_included_in_staked(terra_api, requests_mock):
    requests_mock.get(
        f'{BASE_URL}/cosmos/bank/v1beta1/balances/{ADDRESS}',
        json={'balances': [], 'pagination': {}},
    )
    requests_mock.get(
        f'{BASE_URL}/cosmos/staking/v1beta1/delegations/{ADDRESS}',
        json={
            'delegation_responses': [
                {
                    'delegation': {
                        'delegator_address': ADDRESS,
                        'validator_address': 'terravaloper1test',
                        'shares': '50000000',
                    },
                    'balance': {'denom': 'uluna', 'amount': '50000000'},
                }
            ],
            'pagination': {},
        },
    )
    requests_mock.get(
        f'{BASE_URL}/cosmos/staking/v1beta1/delegators/{ADDRESS}/unbonding_delegations',
        json={
            'unbonding_responses': [
                {
                    'delegator_address': ADDRESS,
                    'validator_address': 'terravaloper1test2',
                    'entries': [
                        {'balance': '25000000', 'completion_time': '2026-04-01'},
                    ],
                }
            ],
            'pagination': {},
        },
    )
    requests_mock.get(
        f'{BASE_URL}/cosmos/distribution/v1beta1/delegators/{ADDRESS}/rewards',
        json={'rewards': [], 'total': []},
    )

    balances = terra_api.get_balance(ADDRESS)
    staked = [b for b in balances if b.asset_type == AssetType.STAKED]
    assert len(staked) == 1
    # 50 delegated + 25 unbonding = 75
    assert staked[0].balance == Decimal('75')
