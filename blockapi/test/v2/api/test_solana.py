import json
from decimal import Decimal
from unittest.mock import call, patch

import pytest
from requests_mock import Mocker

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api import SolanaApi, SolscanApi
from blockapi.v2.base import ApiException
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
    ('rpc_url', 'status', 'retry_after'),
    [
        ('https://proxy/solana/', 429, None),
        ('https://not-helius-rpc.com/', 429, None),
        ('https://helius-rpc.com.example.org/', 429, None),
        ('https://mainnet.helius-rpc.com/', 400, None),
        ('https://mainnet.helius-rpc.com/', 500, None),
        ('https://mainnet.helius-rpc.com/', 429, '5'),
        ('https://mainnet.helius-rpc.com/', 429, 'Fri, 31 Dec 9999 23:59:59 GMT'),
        ('https://mainnet.helius-rpc.com/', 429, 'invalid'),
    ],
)
def test_fetch_does_not_retry_other_errors_or_long_cooldowns(
    rpc_url, status, retry_after
):
    headers = {'Retry-After': retry_after} if retry_after is not None else {}
    with Mocker() as m, patch('time.sleep') as sleep:
        m.post(rpc_url, status_code=status, headers=headers)
        with pytest.raises(ApiException):
            SolanaApi(base_url=rpc_url).fetch_balances('address')

    assert len(m.request_history) == 1
    sleep.assert_not_called()


@pytest.mark.parametrize(
    ('rpc_url', 'uses_v2_staking', 'retry_index', 'retry_after'),
    [
        ('https://mainnet.helius-rpc.com/', True, None, None),
        ('https://proxy/solana/', False, None, None),
        ('https://mainnet.helius-rpc.com/', True, 0, None),
        ('https://mainnet.helius-rpc.com/', True, 1, '0'),
        ('https://mainnet.helius-rpc.com/', True, 2, '1'),
        ('https://mainnet.helius-rpc.com/', True, 3, None),
        ('https://mainnet.helius-rpc.com/', True, 5, None),
    ],
)
def test_get_balance_supports_helius_and_legacy_staking_responses(
    sol_balance_response,
    token_accounts_response,
    das_asset_batch_response,
    staked_solana_response,
    rpc_url,
    uses_v2_staking,
    retry_index,
    retry_after,
):
    test_addr = '5PjMxaijeVVQtuEzxK2NxyJeWwUbpTsi2uXuZ653WoHu'
    empty_token_accounts = '{"jsonrpc":"2.0","result":{"context":{"apiVersion":"1.17.34","slot":268207149},"value":[]},"id":1}'
    staking_response = json.loads(staked_solana_response)
    if not uses_v2_staking:
        staking_response['result'] = staking_response['result']['accounts']

    responses = [
        {'text': data}
        for data in [
            sol_balance_response,
            token_accounts_response,
            empty_token_accounts,
            das_asset_batch_response,
            json.dumps(staking_response),
        ]
    ]
    if uses_v2_staking:
        responses.insert(
            4, {'json': {'result': {'accounts': [], 'paginationKey': 'next-page'}}}
        )
    if retry_index is not None:
        headers = {'Retry-After': retry_after} if retry_after is not None else {}
        responses.insert(retry_index, {'status_code': 429, 'headers': headers})

    with Mocker() as m, patch('time.sleep') as sleep:
        m.post(rpc_url, responses)
        api = SolanaApi(base_url=rpc_url)
        balances = api.get_balance(test_addr)

    if retry_index is not None:
        sleep.assert_called_once_with(1.1)
        assert len(m.request_history) == len(responses)
        assert (
            m.request_history[retry_index].body
            == m.request_history[retry_index + 1].body
        )
    else:
        sleep.assert_not_called()

    staking_balances = {
        balance.asset_type: balance.balance_raw
        for balance in balances
        if balance.asset_type in {AssetType.STAKED, AssetType.LOCKED}
    }
    assert staking_balances == {
        AssetType.STAKED: Decimal('179062913955311'),
        AssetType.LOCKED: Decimal('424045085255'),
    }


@pytest.mark.parametrize('fail_on_same_rpc', [True, False])
def test_retry_is_shared_across_fetch_and_resets_for_next_fetch(
    token_accounts_response, fail_on_same_rpc
):
    api = SolanaApi(base_url='https://mainnet.helius-rpc.com/')
    responses = [{'status_code': 429}]
    if not fail_on_same_rpc:
        responses += [
            {'json': {'result': {'value': 0}}},
            {'text': token_accounts_response},
            {'json': {'result': {'value': []}}},
            {'status_code': 429},  # Optional DAS metadata may fail.
            {'json': {'result': {'accounts': [], 'paginationKey': 'next-page'}}},
        ]
    responses.append({'status_code': 429})

    with Mocker() as m, patch('time.sleep') as sleep:
        for attempt in range(2):
            m.post(api.base_url, responses)
            with pytest.raises(ApiException):
                api.fetch_balances('address')
            assert len(m.request_history) == (attempt + 1) * len(responses)
            if not fail_on_same_rpc:
                assert (
                    m.last_request.json()['params'][1]['paginationKey'] == 'next-page'
                )

    assert sleep.call_args_list == [call(1.1), call(1.1)]


def test_get_coin_retries_helius_metadata_once():
    api = SolanaApi(base_url='https://mainnet.helius-rpc.com/')
    with Mocker() as m, patch('time.sleep') as sleep:
        m.post(api.base_url, [{'status_code': 429}, {'json': {'result': []}}])
        coin = api.get_coin(('mint', 6))

    assert coin.address == 'mint'
    assert len(m.request_history) == 2
    sleep.assert_called_once_with(1.1)


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
            retry=None,
        ),
        call(
            method='getProgramAccountsV2',
            params=[
                api.STAKE_PROGRAM_ID,
                {**config, 'paginationKey': 'next-page'},
            ],
            retry=None,
        ),
        call(
            method='getProgramAccountsV2',
            params=[
                api.STAKE_PROGRAM_ID,
                {**config, 'paginationKey': 'last-page'},
            ],
            retry=None,
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
