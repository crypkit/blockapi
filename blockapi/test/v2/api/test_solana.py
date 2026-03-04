from decimal import Decimal
from unittest.mock import patch

import pytest
from requests_mock import ANY, Mocker

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api import SolanaApi, SolscanApi
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


def test_use_base_url_in_post(
    sol_balance_response,
    token_accounts_response,
    das_asset_batch_response,
    staked_solana_response,
):
    test_addr = '5PjMxaijeVVQtuEzxK2NxyJeWwUbpTsi2uXuZ653WoHu'
    empty_token_accounts = '{"jsonrpc":"2.0","result":{"context":{"apiVersion":"1.17.34","slot":268207149},"value":[]},"id":1}'

    iterator = iter(
        [
            sol_balance_response,
            token_accounts_response,
            empty_token_accounts,
            das_asset_batch_response,
            staked_solana_response,
        ]
    )

    def get_text(*args, **kwargs):
        assert args[0].url == 'https://proxy/solana/'
        data = next(iterator)
        return data

    with Mocker() as m:
        m.post(ANY, text=get_text),
        api = SolanaApi(base_url='https://proxy/solana/')
        api.get_balance(test_addr)


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
