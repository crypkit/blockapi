import json
import logging
from decimal import Decimal
from unittest.mock import call, patch

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.test.v2.api.fake_sleep_provider import FakeSleepProvider
from blockapi.v2.api import SolanaApi, SolscanApi
from blockapi.v2.base import ApiException, InvalidAddressException
from blockapi.v2.models import (
    AssetType,
    BalanceItem,
    Blockchain,
    Coin,
    CoinContract,
    CoinInfo,
)


@pytest.fixture(autouse=True)
def _reset_caches():
    SolanaApi._das_cache = {}
    yield
    SolanaApi._das_cache = {}


def test_merge_balances_with_different_coins(solana_api, balances_with_different_coins):
    merged = solana_api.merge_balances_with_same_coin(balances_with_different_coins)
    assert len(merged) == 2
    assert merged == balances_with_different_coins


def test_merge_balances_with_different_mixed_coins(
    solana_api, balances_with_mixed_coins
):
    merged = solana_api.merge_balances_with_same_coin(balances_with_mixed_coins)
    assert len(merged) == len(balances_with_mixed_coins) - 2  # 3 balances merged into 1

    for merged_item in merged:
        if not merged_item.raw.get("merged"):
            # skip if not our "merged" item
            continue

        assert merged_item.raw == {
            "merged": [
                balances_with_mixed_coins[2].raw,
                balances_with_mixed_coins[3].raw,
                balances_with_mixed_coins[5].raw,
            ]
        }


@pytest.mark.skip(reason='token list responses are too big, skipping')
@pytest.mark.vcr()
@pytest.mark.integration
def test_get_balance(solana_api):
    balances = solana_api.get_balance('FEeSRuEDk8ENZbpzXjn4uHPz3LQijbeKRzhqVr5zPSJ9')
    flux = [
        x
        for x in balances
        if x.coin.address == 'FLUXBmPhT3Fd1EDVFdg46YREqHBeNypn1h4EbnTzWERX'
    ]
    assert len(flux) == 1
    assert len(balances) == 29


def test_use_custom_url():
    api = SolanaApi(base_url='https://proxy/solana/')
    assert api.base_url == 'https://proxy/solana/'
    assert api.api_options.base_url == 'https://api.mainnet-beta.solana.com/'


def test_use_base_url():
    api = SolanaApi()
    assert api.base_url == 'https://api.mainnet-beta.solana.com/'


@pytest.mark.parametrize(
    ('rpc_url', 'uses_v2_staking', 'throttled_request_index'),
    [
        ('https://mainnet.helius-rpc.com/', True, None),
        ('https://proxy/solana/', False, None),
        ('https://mainnet.helius-rpc.com/', True, 0),
        ('https://mainnet.helius-rpc.com/', True, 1),
        ('https://mainnet.helius-rpc.com/', True, 2),
        ('https://mainnet.helius-rpc.com/', True, 3),
        ('https://mainnet.helius-rpc.com/', True, 4),
    ],
)
def test_get_balance_supports_helius_and_legacy_staking_responses(
    requests_mock,
    sol_balance_response,
    token_accounts_response,
    das_asset_batch_response,
    staked_solana_response,
    rpc_url,
    uses_v2_staking,
    throttled_request_index,
    caplog,
):
    test_addr = '5PjMxaijeVVQtuEzxK2NxyJeWwUbpTsi2uXuZ653WoHu'
    empty_token_accounts = '{"jsonrpc":"2.0","result":{"context":{"apiVersion":"1.17.34","slot":268207149},"value":[]},"id":1}'
    staking_response = json.loads(staked_solana_response)
    if not uses_v2_staking:
        staking_response['result'] = staking_response['result']['accounts']

    responses = [
        {'text': sol_balance_response},
        {'text': token_accounts_response},
        {'text': empty_token_accounts},
        {'text': das_asset_batch_response},
        {'json': staking_response},
    ]
    if throttled_request_index is not None:
        responses.insert(
            throttled_request_index,
            {'status_code': 429, 'text': 'Too Many Requests'},
        )
    requests_mock.post(rpc_url, responses)
    sleep_provider = FakeSleepProvider()

    with patch('time.sleep') as sleep:
        api = SolanaApi(base_url=rpc_url, sleep_provider=sleep_provider)
        balances = api.get_balance(test_addr)

    expected_methods = [
        'getBalance',
        'getTokenAccountsByOwner',
        'getTokenAccountsByOwner',
        'getAssetBatch',
        'getProgramAccountsV2' if uses_v2_staking else 'getProgramAccounts',
    ]
    if throttled_request_index is not None:
        retry_index = throttled_request_index
        expected_methods.insert(retry_index, expected_methods[retry_index])
        assert (
            requests_mock.request_history[retry_index].json()
            == requests_mock.request_history[retry_index + 1].json()
        )
        sleep.assert_called_once()
        assert 1 <= sleep.call_args.args[0] <= 1.25
    else:
        sleep.assert_not_called()
    assert [
        r.json()['method'] for r in requests_mock.request_history
    ] == expected_methods
    assert sleep_provider.calls == []
    assert not any(record.levelno >= logging.ERROR for record in caplog.records)

    staking_balances = {
        balance.asset_type: balance.balance_raw
        for balance in balances
        if balance.asset_type in {AssetType.STAKED, AssetType.LOCKED}
    }
    assert staking_balances == {
        AssetType.STAKED: Decimal('179062913955311'),
        AssetType.LOCKED: Decimal('424045085255'),
    }


def test_get_balance_fails_after_three_throttled_token_attempts(requests_mock):
    rpc_url = 'https://mainnet.helius-rpc.com/'
    requests_mock.post(
        rpc_url,
        [
            {'json': {'result': {'value': 1}}},
            {'status_code': 429, 'text': 'Too Many Requests'},
        ],
    )
    sleep_provider = FakeSleepProvider()
    api = SolanaApi(base_url=rpc_url, sleep_provider=sleep_provider)

    with patch('time.sleep') as sleep, pytest.raises(ApiException, match='429'):
        api.get_balance('address')

    assert [r.json()['method'] for r in requests_mock.request_history] == [
        'getBalance',
        'getTokenAccountsByOwner',
        'getTokenAccountsByOwner',
        'getTokenAccountsByOwner',
    ]
    assert sleep_provider.calls == []
    assert len(sleep.call_args_list) == 2
    assert 1 <= sleep.call_args_list[0].args[0] <= 1.25
    assert 2 <= sleep.call_args_list[1].args[0] <= 2.25


@pytest.mark.parametrize(
    ('retry_after', 'min_delays'),
    [
        (None, [1]),
        pytest.param(None, [1, 2], id='success-on-third-attempt'),
        ('2', [2]),
        ('5', [5]),
        ('0', [1]),
        ('-1', [1]),
        ('invalid', [1]),
        ('Thu, 10 Sep 2026 07:00:03 GMT', [3]),
        ('Thu, 10 Sep 2026 06:59:59 GMT', [1]),
    ],
)
def test_helius_retry_after_without_sleep_provider(
    requests_mock, retry_after, min_delays
):
    rpc_url = 'https://mainnet.helius-rpc.com/?api-key=test-key'
    headers = {'Retry-After': retry_after} if retry_after is not None else {}
    requests_mock.post(
        rpc_url,
        [
            {'status_code': 429, 'text': 'Too Many Requests', 'headers': headers},
        ]
        * len(min_delays)
        + [{'json': {'result': {'value': 1}}}],
    )
    api = SolanaApi(base_url=rpc_url)

    with patch('time.sleep') as sleep, patch('time.time', return_value=1789023600):
        result = api._request('getBalance', ['address'])

    assert result == {'result': {'value': 1}}
    assert requests_mock.call_count == len(min_delays) + 1
    assert sleep.call_count == len(min_delays)
    for sleep_call, min_delay in zip(sleep.call_args_list, min_delays):
        assert min_delay <= sleep_call.args[0] <= min(min_delay + 0.25, 5)
    assert all(
        request.json() == requests_mock.request_history[0].json()
        for request in requests_mock.request_history[1:]
    )


@pytest.mark.parametrize('retry_after', ['6', '60', 'Thu, 10 Sep 2026 07:01:00 GMT'])
def test_helius_long_retry_after_fails_without_early_retry(requests_mock, retry_after):
    rpc_url = 'https://mainnet.helius-rpc.com/'
    requests_mock.post(
        rpc_url,
        status_code=429,
        text='Too Many Requests',
        headers={'Retry-After': retry_after},
    )
    api = SolanaApi(base_url=rpc_url)

    with patch('time.sleep') as sleep, patch('time.time', return_value=1789023600):
        with pytest.raises(ApiException, match='429'):
            api.get_balance('address')

    assert requests_mock.call_count == 1
    sleep.assert_not_called()


@pytest.mark.parametrize('status_code', [400, 401, 403, 500, 503])
def test_helius_does_not_retry_other_http_errors(requests_mock, status_code):
    rpc_url = 'https://mainnet.helius-rpc.com/'
    requests_mock.post(rpc_url, status_code=status_code, text='RPC unavailable')
    api = SolanaApi(base_url=rpc_url)

    with patch('time.sleep') as sleep:
        with pytest.raises(ApiException, match=str(status_code)):
            api.get_balance('address')

    assert requests_mock.call_count == 1
    sleep.assert_not_called()


def test_helius_keeps_invalid_address_error(requests_mock):
    rpc_url = 'https://mainnet.helius-rpc.com/'
    requests_mock.post(
        rpc_url,
        json={'error': {'code': -32602, 'message': 'Invalid param: WrongSize'}},
    )
    api = SolanaApi(base_url=rpc_url)

    with patch('time.sleep') as sleep, pytest.raises(InvalidAddressException):
        api.get_balance('invalid')

    assert requests_mock.call_count == 1
    sleep.assert_not_called()


@pytest.mark.parametrize(
    'rpc_url', ['https://proxy/solana/', 'https://helius-rpc.com.example.org/']
)
def test_non_helius_throttling_keeps_existing_behavior(requests_mock, rpc_url):
    requests_mock.post(rpc_url, status_code=429, text='Too Many Requests')
    sleep_provider = FakeSleepProvider()
    api = SolanaApi(base_url=rpc_url, sleep_provider=sleep_provider)

    with patch('time.sleep') as sleep, pytest.raises(ApiException, match='429'):
        api.get_balance('address')

    assert requests_mock.call_count == 1
    assert sleep_provider.calls == []
    sleep.assert_not_called()


def test_helius_retries_staking_page_without_duplicate_accounts(requests_mock):
    rpc_url = 'https://mainnet.helius-rpc.com/'
    requests_mock.post(
        rpc_url,
        [
            {
                'json': {
                    'result': {
                        'accounts': [{'pubkey': 'first'}],
                        'paginationKey': 'next',
                    }
                }
            },
            {'status_code': 429, 'text': 'Too Many Requests'},
            {
                'json': {
                    'result': {
                        'accounts': [{'pubkey': 'second'}],
                        'paginationKey': None,
                    }
                }
            },
        ],
    )
    api = SolanaApi(base_url=rpc_url)

    with patch('time.sleep'):
        result = api._fetch_staked_sol('address')

    assert result['result'] == [{'pubkey': 'first'}, {'pubkey': 'second'}]
    assert requests_mock.call_count == 3
    assert 'paginationKey' not in requests_mock.request_history[0].json()['params'][1]
    retry_body = requests_mock.request_history[1].json()
    assert retry_body['params'][1]['paginationKey'] == 'next'
    assert requests_mock.request_history[2].json() == retry_body


def test_build_coin_from_das_asset():
    api = SolanaApi()
    asset = {
        'id': 'J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn',
        'interface': 'FungibleToken',
        'content': {
            'metadata': {
                'name': 'Jito Staked SOL',
                'symbol': 'JITOSOL',
            },
            'links': {
                'image': 'https://example.com/jitosol.png',
            },
        },
        'token_info': {
            'decimals': 9,
            'symbol': 'JITOSOL',
        },
    }

    coin = api._build_coin_from_das_asset(asset)
    assert coin.symbol == 'JITOSOL'
    assert coin.name == 'Jito Staked SOL'
    assert coin.decimals == 9
    assert coin.blockchain == Blockchain.SOLANA
    assert coin.address == 'J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn'
    assert coin.info.logo_url == 'https://example.com/jitosol.png'
    assert coin.is_nft is False
    assert 'FungibleToken' in coin.standards


def test_nft_skipped_when_include_nfts_false():
    api = SolanaApi(include_nfts=False)
    asset = {
        'id': 'NFTmint123',
        'interface': 'V1_NFT',
        'content': {
            'metadata': {
                'name': 'Cool NFT',
                'symbol': 'CNFT',
            },
            'links': {},
        },
        'token_info': {
            'decimals': 0,
        },
    }

    coin = api._build_coin_from_das_asset(asset)
    assert coin is not None
    assert coin.is_nft is True


def test_nft_included_when_include_nfts_true():
    api = SolanaApi(include_nfts=True)
    asset = {
        'id': 'NFTmint123',
        'interface': 'V1_NFT',
        'content': {
            'metadata': {
                'name': 'Cool NFT',
                'symbol': 'CNFT',
            },
            'links': {
                'image': 'https://example.com/nft.png',
            },
        },
        'token_info': {
            'decimals': 0,
        },
    }

    coin = api._build_coin_from_das_asset(asset)
    assert coin is not None
    assert coin.symbol == 'CNFT'
    assert coin.name == 'Cool NFT'
    assert coin.is_nft is True
    assert 'V1_NFT' in coin.standards


def test_parse_staked_balance_skips_undelegated():
    api = SolanaApi()
    response = {
        'result': [
            # Delegated account with stake
            {
                'account': {
                    'lamports': 2282880,
                    'data': {
                        'parsed': {
                            'info': {
                                'stake': {
                                    'delegation': {
                                        'stake': '1000000000',
                                    }
                                }
                            }
                        }
                    },
                }
            },
            # Undelegated account: stake key is null
            {
                'account': {
                    'lamports': 2282880,
                    'data': {
                        'parsed': {
                            'info': {
                                'stake': None,
                            }
                        }
                    },
                }
            },
            # Undelegated account: stake key absent
            {
                'account': {
                    'lamports': 2282880,
                    'data': {
                        'parsed': {
                            'info': {},
                        }
                    },
                }
            },
        ]
    }
    result = api._parse_staked_balance(response)
    assert result is not None
    assert result.balance_raw == 1000000000
    assert result.asset_type == AssetType.STAKED


def test_fetch_staked_sol_uses_v2_pagination():
    api = SolanaApi(base_url='https://mainnet.helius-rpc.com/')
    address = '5PjMxaijeVVQtuEzxK2NxyJeWwUbpTsi2uXuZ653WoHu'
    first_account = {'pubkey': 'first'}
    second_account = {'pubkey': 'second'}

    with patch.object(
        api,
        '_request',
        side_effect=[
            {
                'jsonrpc': '2.0',
                'id': 1,
                'result': {
                    'accounts': [first_account],
                    'paginationKey': 'next-page',
                },
            },
            {
                'jsonrpc': '2.0',
                'id': 2,
                'result': {
                    'accounts': [],
                    'paginationKey': 'last-page',
                },
            },
            {
                'jsonrpc': '2.0',
                'id': 3,
                'result': {
                    'accounts': [second_account],
                    'paginationKey': None,
                },
            },
        ],
    ) as request:
        response = api._fetch_staked_sol(address)

    config = {
        'filters': [
            {
                'memcmp': {
                    'offset': api.STAKE_AUTHORITY_OFFSET,
                    'bytes': address,
                    'encoding': 'base58',
                }
            }
        ],
        'encoding': 'jsonParsed',
        'commitment': 'finalized',
        'limit': api.HELIUS_PROGRAM_ACCOUNTS_PAGE_SIZE,
    }
    assert request.call_args_list == [
        call(
            method='getProgramAccountsV2',
            params=[api.STAKE_PROGRAM_ID, config],
        ),
        call(
            method='getProgramAccountsV2',
            params=[
                api.STAKE_PROGRAM_ID,
                {**config, 'paginationKey': 'next-page'},
            ],
        ),
        call(
            method='getProgramAccountsV2',
            params=[
                api.STAKE_PROGRAM_ID,
                {**config, 'paginationKey': 'last-page'},
            ],
        ),
    ]
    assert response == {
        'jsonrpc': '2.0',
        'id': 3,
        'result': [first_account, second_account],
    }


def test_fetch_staked_sol_rejects_repeated_pagination_key():
    api = SolanaApi(base_url='https://mainnet.helius-rpc.com/')
    repeated_page = {
        'result': {
            'accounts': [],
            'paginationKey': 'same-page',
        }
    }
    terminal_page = {
        'result': {
            'accounts': [],
            'paginationKey': None,
        }
    }

    with patch.object(
        api,
        '_request',
        side_effect=[repeated_page, repeated_page, terminal_page],
    ) as request:
        with pytest.raises(ApiException, match='repeated pagination key'):
            api._fetch_staked_sol('address')

    assert request.call_count == 2


def test_fetch_staked_sol_uses_legacy_method_for_non_helius_rpc():
    api = SolanaApi()

    with patch.object(api, '_request', return_value={'result': []}) as request:
        response = api._fetch_staked_sol('address')

    request.assert_called_once()
    assert request.call_args.kwargs['method'] == 'getProgramAccounts'
    assert 'limit' not in request.call_args.kwargs['params'][1]
    assert response == {'result': []}


def test_das_cache_stores_sentinel_for_unknown_mint():
    api = SolanaApi()
    unknown_mint = 'UnknownMint111111111111111111111111111111111'

    with patch.object(
        api,
        '_request',
        return_value={'result': []},
    ):
        api._fetch_das_assets([unknown_mint])

    assert unknown_mint in api._das_cache
    assert api._das_cache[unknown_mint] == {}


def test_das_cache_prevents_refetch():
    api = SolanaApi()
    # Pre-populate cache
    api._das_cache['mint1'] = {
        'id': 'mint1',
        'interface': 'FungibleToken',
        'content': {'metadata': {'name': 'Token1', 'symbol': 'TK1'}, 'links': {}},
        'token_info': {'decimals': 6},
    }
    # _fetch_das_assets should skip cached mint
    with patch.object(api, '_request') as mock_request:
        api._fetch_das_assets(['mint1'])
        mock_request.assert_not_called()


def test_solscan_get_staked_balance(requests_mock, solscan_staked_response):
    test_addr = '5PjMxaijeVVQtuEzxK2NxyJeWwUbpTsi2uXuZ653WoHu'
    requests_mock.get(
        f'https://api.solscan.io/account/stake?address={test_addr}',
        json=solscan_staked_response,
    )

    staked_balance = SolscanApi().get_staked_balance(test_addr)
    assert staked_balance.asset_type == AssetType.STAKED
    assert staked_balance.balance == Decimal('55663.568093516')


@pytest.fixture
def solscan_staked_response():
    return {
        "success": True,
        "data": {
            "5Z9j4ewQsHovszAc5F1jiANLsX3412a5Bzkxx8Gwmjs": {
                "voter": "26pV97Ce83ZQ6Kz9XT4td8tdoUFPTng8Fb8gPyc53dJx",
                "amount": "22033088837332",
                "type": "delegated",
                "stakeAccount": "5Z9j4ewQsHovszAc5F1jiANLsX3412a5Bzkxx8Gwmjs",
                "staker": "5PjMxaijeVVQtuEzxK2NxyJeWwUbpTsi2uXuZ653WoHu",
                "role": ["staker", "withdrawer"],
            },
            "AcfWTCgwhcTqKiiAbATi9jvbnAsJLA1s6YqSptsY7BWW": {
                "voter": "J2nUHEAgZFRyuJbFjdqPrAa9gyWDuc7hErtDQHPhsYRp",
                "amount": "33630479256184",
                "type": "delegated",
                "stakeAccount": "AcfWTCgwhcTqKiiAbATi9jvbnAsJLA1s6YqSptsY7BWW",
                "staker": "5PjMxaijeVVQtuEzxK2NxyJeWwUbpTsi2uXuZ653WoHu",
                "role": ["staker"],
            },
        },
    }


@pytest.fixture()
def balances_with_mixed_coins():
    return [
        BalanceItem(
            balance=Decimal('1'),
            balance_raw=Decimal('1'),
            raw={},
            coin=Coin(
                symbol='COIN1',
                name='unknown',
                decimals=0,
                blockchain=Blockchain.SOLANA,
                address='addr1',
                standards=None,
                protocol_id=None,
                info=None,
            ),
            asset_type=AssetType.AVAILABLE,
            last_updated=None,
            protocol=None,
            is_wallet=True,
        ),
        BalanceItem(
            balance=Decimal('11'),
            balance_raw=Decimal('11'),
            raw={},
            coin=Coin(
                symbol='COIN2',
                name='unknown',
                decimals=0,
                blockchain=Blockchain.SOLANA,
                address='addr2',
                standards=None,
                protocol_id=None,
                info=None,
            ),
            asset_type=AssetType.AVAILABLE,
            last_updated=None,
            protocol=None,
            is_wallet=True,
        ),
        BalanceItem(
            balance=Decimal('1'),
            balance_raw=Decimal('1'),
            raw={"raw1": "raw1"},
            coin=Coin(
                symbol='unknown',
                name='unknown',
                decimals=0,
                blockchain=Blockchain.SOLANA,
                address='HEL6KGUEvwYgTtcjenf9qeAb2Zg9Yr77usWPY9UZvoQj',
                standards=None,
                protocol_id=None,
                info=None,
            ),
            asset_type=AssetType.AVAILABLE,
            last_updated=None,
            protocol=None,
            is_wallet=True,
        ),
        BalanceItem(
            balance=Decimal('11'),
            balance_raw=Decimal('11'),
            raw={"raw2": "raw2"},
            coin=Coin(
                symbol='unknown',
                name='unknown',
                decimals=0,
                blockchain=Blockchain.SOLANA,
                address='HEL6KGUEvwYgTtcjenf9qeAb2Zg9Yr77usWPY9UZvoQj',
                standards=None,
                protocol_id=None,
                info=None,
            ),
            asset_type=AssetType.AVAILABLE,
            last_updated=None,
            protocol=None,
            is_wallet=True,
        ),
        BalanceItem(
            balance=Decimal('99'),
            balance_raw=Decimal('99'),
            raw={},
            coin=Coin(
                symbol='COIN3',
                name='unknown',
                decimals=0,
                blockchain=Blockchain.SOLANA,
                address='addr3',
                standards=None,
                protocol_id=None,
                info=None,
            ),
            asset_type=AssetType.AVAILABLE,
            last_updated=None,
            protocol=None,
            is_wallet=True,
        ),
        BalanceItem(
            balance=Decimal('11'),
            balance_raw=Decimal('11'),
            raw={"raw3": "raw3"},
            coin=Coin(
                symbol='unknown',
                name='unknown',
                decimals=0,
                blockchain=Blockchain.SOLANA,
                address='HEL6KGUEvwYgTtcjenf9qeAb2Zg9Yr77usWPY9UZvoQj',
                standards=None,
                protocol_id=None,
                info=None,
            ),
            asset_type=AssetType.AVAILABLE,
            last_updated=None,
            protocol=None,
            is_wallet=True,
        ),
    ]


@pytest.fixture
def sol_balance_response():
    return '{"jsonrpc":"2.0","result":{"context":{"apiVersion":"1.17.34","slot":268207149},"value":0},"id":1}'


@pytest.fixture
def token_accounts_response():
    return read_file('data/solana/token_accounts_response.json')


@pytest.fixture
def das_asset_batch_response():
    return read_file('data/solana/das_get_asset_batch_response.json')


@pytest.fixture
def staked_solana_response():
    return read_file('data/solana/staked_solana_response.json')


@pytest.fixture
def solana_api():
    return SolanaApi()


@pytest.fixture()
def balances_with_same_coin():
    return [
        BalanceItem(
            balance=Decimal('1'),
            balance_raw=Decimal('1'),
            raw={'raw1': 'raw_value_1'},
            coin=Coin(
                symbol='unknown',
                name='unknown',
                decimals=0,
                blockchain=Blockchain.SOLANA,
                address='HEL6KGUEvwYgTtcjenf9qeAb2Zg9Yr77usWPY9UZvoQj',
                standards=None,
                protocol_id=None,
                info=None,
            ),
            asset_type=AssetType.AVAILABLE,
            last_updated=None,
            protocol=None,
            is_wallet=True,
        ),
        BalanceItem(
            balance=Decimal('11'),
            balance_raw=Decimal('11'),
            raw={'raw2': 'raw_value_2'},
            coin=Coin(
                symbol='unknown',
                name='unknown',
                decimals=0,
                blockchain=Blockchain.SOLANA,
                address='HEL6KGUEvwYgTtcjenf9qeAb2Zg9Yr77usWPY9UZvoQj',
                standards=None,
                protocol_id=None,
                info=None,
            ),
            asset_type=AssetType.AVAILABLE,
            last_updated=None,
            protocol=None,
            is_wallet=True,
        ),
    ]


def test_merge_balances_with_same_coin(solana_api, balances_with_same_coin):
    merged = solana_api.merge_balances_with_same_coin(balances_with_same_coin)
    assert len(merged) == 1

    merged = merged[0]
    assert merged.balance == 12
    assert merged.balance_raw == 12
    assert merged.raw == {
        "merged": [balances_with_same_coin[0].raw, balances_with_same_coin[1].raw]
    }


@pytest.fixture()
def balances_with_different_coins():
    return [
        BalanceItem(
            balance=Decimal('1'),
            balance_raw=Decimal('1'),
            raw={
                'account': {
                    'data': {
                        'parsed': {
                            'info': {
                                'isNative': False,
                                'mint': 'HEL6KGUEvwYgTtcjenf9qeAb2Zg9Yr77usWPY9UZvoQj',
                                'owner': 'FEeSRuEDk8ENZbpzXjn4uHPz3LQijbeKRzhqVr5zPSJ9',
                                'state': 'initialized',
                                'tokenAmount': {
                                    'amount': '1',
                                    'decimals': 0,
                                    'uiAmount': 1.0,
                                    'uiAmountString': '1',
                                },
                            },
                            'type': 'account',
                        },
                        'program': 'spl-token',
                        'space': 165,
                    },
                    'executable': False,
                    'lamports': 2039280,
                    'owner': 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA',
                    'rentEpoch': 332,
                },
                'pubkey': 'FxNFQw1sdtuhYtbhnd9HfUabDoW9rrTPuDFkzTQv7DQi',
            },
            coin=Coin(
                symbol='COIN1',
                name='unknown',
                decimals=0,
                blockchain=Blockchain.SOLANA,
                address='addr1',
                standards=None,
                protocol_id=None,
                info=CoinInfo(tags=["tags", "test"]),
            ),
            asset_type=AssetType.AVAILABLE,
            last_updated=None,
            protocol=None,
            is_wallet=True,
        ),
        BalanceItem(
            balance=Decimal('11'),
            balance_raw=Decimal('11'),
            raw={
                'account': {
                    'data': {
                        'parsed': {
                            'info': {
                                'isNative': False,
                                'mint': 'HEL6KGUEvwYgTtcjenf9qeAb2Zg9Yr77usWPY9UZvoQj',
                                'owner': 'FEeSRuEDk8ENZbpzXjn4uHPz3LQijbeKRzhqVr5zPSJ9',
                                'state': 'initialized',
                                'tokenAmount': {
                                    'amount': '11',
                                    'decimals': 0,
                                    'uiAmount': 11.0,
                                    'uiAmountString': '11',
                                },
                            },
                            'type': 'account',
                        },
                        'program': 'spl-token',
                        'space': 165,
                    },
                    'executable': False,
                    'lamports': 2039280,
                    'owner': 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA',
                    'rentEpoch': 333,
                },
                'pubkey': '3XwuM1fhKPmH9onVgtTu8SwC7pPxnKWkUYqqks7NaWPF',
            },
            coin=Coin(
                symbol='COIN2',
                name='unknown',
                decimals=0,
                blockchain=Blockchain.SOLANA,
                address='addr2',
                standards=None,
                protocol_id=None,
                info=None,
            ),
            asset_type=AssetType.AVAILABLE,
            last_updated=None,
            protocol=None,
            is_wallet=True,
        ),
    ]


def test_merge_balances_contract_merge(solana_api):
    balances = [
        BalanceItem(
            **{
                'balance': Decimal('1'),
                'balance_raw': Decimal('1'),
                'coin': None,
                'coin_contract': CoinContract(
                    **{
                        'blockchain': 'solana',
                        'contract': 'HEL6KGUEvwYgTtcjenf9qeAb2Zg9Yr77usWPY9UZvoQj',
                        'decimals': 0,
                    }
                ),
                'raw': {},
                'asset_type': 'available',
                'last_updated': None,
                'protocol': None,
                'is_wallet': True,
                'pool_info': None,
            }
        ),
        BalanceItem(
            **{
                'balance': Decimal('11'),
                'balance_raw': Decimal('11'),
                'coin': None,
                'coin_contract': CoinContract(
                    **{
                        'blockchain': 'solana',
                        'contract': 'HEL6KGUEvwYgTtcjenf9qeAb2Zg9Yr77usWPY9UZvoQj',
                        'decimals': 0,
                    }
                ),
                'raw': {},
                'asset_type': 'available',
                'last_updated': None,
                'protocol': None,
                'is_wallet': True,
                'pool_info': None,
            }
        ),
    ]

    merged = solana_api.merge_balances_with_same_coin(balances)
    assert len(merged) == 1
    assert merged[0].coin_contract is not None
