import json
from decimal import Decimal

import pytest
import requests_mock

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api import SolanaApi, SolscanApi
from blockapi.v2.models import AssetType, BalanceItem, Blockchain, Coin, CoinInfo


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


def test_merge_balances_with_different_coins(solana_api, balances_with_different_coins):
    merged = solana_api.merge_balances_with_same_coin(balances_with_different_coins)
    assert len(merged) == 2
    assert merged == balances_with_different_coins


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
def solana_response():
    return read_file('data/solana_response.json')


@pytest.fixture
def solana_tokenlist():
    return read_file('data/solana_tokenlist.json')


@pytest.fixture
def solana_value_response():
    return json.dumps(dict(result=dict(value=0)))


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


@pytest.mark.vcr()
@pytest.mark.integration
def test_get_balance(solana_api):
    balances = solana_api.get_balance('FEeSRuEDk8ENZbpzXjn4uHPz3LQijbeKRzhqVr5zPSJ9')
    assert len(balances) > 200

    merged_balance = []
    for item in balances:
        if item.coin.address == 'HEL6KGUEvwYgTtcjenf9qeAb2Zg9Yr77usWPY9UZvoQj':
            merged_balance.append(item)

    assert len(merged_balance) == 1
    merged_balance = merged_balance[0]
    assert len(merged_balance.raw.get("merged")) == 2


def test_use_custom_url():
    api = SolanaApi(base_url='https://proxy/solana/')
    assert api.base_url == 'https://proxy/solana/'
    assert api.api_options.base_url == 'https://api.mainnet-beta.solana.com/'


def test_use_base_url():
    api = SolanaApi()
    assert api.base_url == 'https://api.mainnet-beta.solana.com/'


def test_use_base_url_in_post(solana_value_response, solana_response, solana_tokenlist):
    test_addr = '5PjMxaijeVVQtuEzxK2NxyJeWwUbpTsi2uXuZ653WoHu'

    iterator = iter([solana_value_response, solana_response])

    def get_text(*args, **kwargs):
        assert args[0].url == 'https://proxy/solana/'
        data = next(iterator)
        return data

    with requests_mock.Mocker() as m:
        m.get(
            'https://raw.githubusercontent.com/solana-labs/token-list/main/src/tokens/solana.tokenlist.json',
            text=solana_tokenlist,
        )
        m.post(requests_mock.ANY, text=get_text),
        api = SolanaApi(base_url='https://proxy/solana/')
        api.get_balance(test_addr)


def test_solscan_get_staked_balance(requests_mock):
    test_addr = '5PjMxaijeVVQtuEzxK2NxyJeWwUbpTsi2uXuZ653WoHu'
    requests_mock.get(
        f'https://api.solscan.io/account/stake?address={test_addr}',
        json=solscan_staked_response,
    )

    staked_balance = SolscanApi().get_staked_balance(test_addr)
    assert staked_balance.asset_type == AssetType.STAKED
    assert staked_balance.balance == Decimal('55663.568093516')


solscan_staked_response = {
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
