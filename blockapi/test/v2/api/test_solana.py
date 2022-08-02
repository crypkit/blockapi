from decimal import Decimal

import pytest

from blockapi.v2.api.solana import SolanaApi
from blockapi.v2.models import AssetType, BalanceItem, Blockchain, Coin


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
        balances_with_same_coin[0].coin.address: balances_with_same_coin[0].raw,
        balances_with_same_coin[1].coin.address: balances_with_same_coin[1].raw,
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
    ]


def test_merge_balances_with_different_mixed_coins(
    solana_api, balances_with_mixed_coins
):
    merged = solana_api.merge_balances_with_same_coin(balances_with_mixed_coins)
    assert len(merged) == len(balances_with_mixed_coins) - 1
