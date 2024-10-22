import json
from decimal import Decimal

import pytest
from requests_mock import ANY, Mocker
from solders.pubkey import Pubkey

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api import SolanaApi, SolscanApi
from blockapi.v2.api.solana import (
    JUP_AG_BAN_LIST_URL,
    JUP_AG_TOKEN_LIST_URL,
    SOL_TOKEN_LIST_URL,
    SONAR_TOKEN_LIST_URL,
)
from blockapi.v2.models import AssetType, BalanceItem, Blockchain, Coin, CoinInfo


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
    solana_value_response,
    solana_response,
    staked_solana_response,
    rent_reserve_solana_response,
    token_list_sol_response,
    token_list_jup_ag_response,
    token_list_sonar_response,
    ban_list_jup_ag_response,
):
    test_addr = '5PjMxaijeVVQtuEzxK2NxyJeWwUbpTsi2uXuZ653WoHu'

    iterator = iter(
        [
            solana_value_response,
            solana_response,
            '{"result": {"value": []}}',
            staked_solana_response,
            rent_reserve_solana_response,
        ]
    )

    def get_text(*args, **kwargs):
        assert args[0].url == 'https://proxy/solana/'
        data = next(iterator)
        return data

    with Mocker() as m:
        m.get(SOL_TOKEN_LIST_URL, text=token_list_sol_response)
        m.get(JUP_AG_TOKEN_LIST_URL, text=token_list_jup_ag_response)
        m.get(SONAR_TOKEN_LIST_URL, text=token_list_sonar_response)
        m.get(JUP_AG_BAN_LIST_URL, text=ban_list_jup_ag_response)
        m.post(ANY, text=get_text),
        api = SolanaApi(base_url='https://proxy/solana/', fetch_metaplex=False)
        api.get_balance(test_addr)


def test_create_token(
    requests_mock,
    token_list_sol_response,
    token_list_jup_ag_response,
    token_list_sonar_response,
    ban_list_jup_ag_response,
):
    requests_mock.get(SOL_TOKEN_LIST_URL, text=token_list_sol_response)
    requests_mock.get(JUP_AG_TOKEN_LIST_URL, text=token_list_jup_ag_response)
    requests_mock.get(SONAR_TOKEN_LIST_URL, text=token_list_sonar_response)
    requests_mock.get(JUP_AG_BAN_LIST_URL, text=ban_list_jup_ag_response)

    coin = SolanaApi().get_token_data('J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn')
    assert coin.symbol == 'JITOSOL'
    assert coin.name == 'Jito Staked SOL'
    assert coin.decimals == 9
    assert coin.blockchain == Blockchain.SOLANA
    assert coin.address == 'J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn'


def test_map_mplx_token(
    requests_mock,
    token_list_sol_response,
    token_list_jup_ag_response,
    token_list_sonar_response,
    ban_list_jup_ag_response,
):
    requests_mock.get(SOL_TOKEN_LIST_URL, text=token_list_sol_response)
    requests_mock.get(JUP_AG_TOKEN_LIST_URL, text=token_list_jup_ag_response)
    requests_mock.get(SONAR_TOKEN_LIST_URL, text=token_list_sonar_response)
    requests_mock.get(JUP_AG_BAN_LIST_URL, text=ban_list_jup_ag_response)

    coin = SolanaApi().get_token_data('METAewgxyPbgwsseH8T16a39CQ5VyVxZi9zXiDPY18m')
    assert coin.symbol == 'MPLX'
    assert coin.decimals == 6
    assert coin.blockchain == Blockchain.SOLANA
    assert coin.address == 'METAewgxyPbgwsseH8T16a39CQ5VyVxZi9zXiDPY18m'


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
def solana_response():
    return read_file('data/solana/solana_response.json')


@pytest.fixture
def solana_value_response():
    return json.dumps(dict(result=dict(value=0)))


@pytest.fixture
def staked_solana_response():
    return read_file('data/solana/staked_solana_response.json')


@pytest.fixture
def rent_reserve_solana_response():
    return read_file('data/solana/rent_reserve_solana_response.json')


@pytest.fixture
def token_list_sol_response():
    return read_file('data/solana/token-list-solana.json')


@pytest.fixture
def token_list_jup_ag_response():
    return read_file('data/solana/token-list-jup-ag.csv')


@pytest.fixture
def token_list_sonar_response():
    return read_file('data/solana/token-list-sonar.json')


@pytest.fixture
def ban_list_jup_ag_response():
    return read_file('data/solana/ban-list-jup-ag.csv')


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


def test_derive_metaplex_account_address_from_mint(solana_api):
    mint = 'C2PxCHLeDkp1BsG1uueu7aGEfXQkKoXxzTgMPQ5DA6QW'
    metadata = solana_api.get_metadata_pda(mint)

    assert metadata == '3G5bT5bgpdwiUbYHfoBSe6SDAwiQaTKc3TFGks7bA3Qw'


@pytest.mark.vcr()
def test_fetch_metaplex_account(solana_api, metaplex_content):
    data = solana_api.fetch_metaplex_account(
        '3G5bT5bgpdwiUbYHfoBSe6SDAwiQaTKc3TFGks7bA3Qw'
    )
    assert data == metaplex_content


@pytest.mark.vcr()
def test_parse_metaplex_account(solana_api, metaplex_content):
    token = solana_api.parse_metaplex_account(metaplex_content, decimals=9)
    assert token['symbol'] == 'ACT'
    assert token['name'] == 'Act I : The AI Prophecy'
    assert token['decimals'] == 9
    assert token['chainId'] == 101
    assert token['tags'] == ['SOLANA', 'MEME']
    assert (
        token['logoURI']
        == 'https://gateway.pinata.cloud/ipfs/QmS4m4cBjukg7YhimqhfRUb2pUE4bBPXbrbMBb5hzxNbUA'
    )


@pytest.fixture
def metaplex_content():
    return (
        'BJ5okXRntUEewuGiuQOIMWt8+YkvFnY7/DoghPyz5qwNo8wWpzohlcKPjWIDCl3nggGst3'
        'CeFvU+P1wA6yNMhm8gAAAAQWN0IEkgOiBUaGUgQUkgUHJvcGhlY3kAAAAAAAAAAAAKAAAA'
        'QUNUAAAAAAAAAMgAAABodHRwczovL2dhdGV3YXkucGluYXRhLmNsb3VkL2lwZnMvUW1WZk'
        '1QQ1VQczVWMW9tYUR2b25pMzh3OGFFSnBGVGpFWlJOUm1vVnlleFhXZQAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAf4BAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQ=='
    )
