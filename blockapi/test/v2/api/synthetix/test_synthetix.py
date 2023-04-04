from decimal import Decimal
from unittest.mock import patch

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api.synthetix import (
    SynthetixMainnetApi,
    SynthetixOptimismApi,
    snx_contract_address,
)
from blockapi.v2.models import AssetType, BalanceItem, Blockchain, Coin

test_address = '0xE2e4F2A725E42D0F0EF6291F46c430F963482001'
contract_name = 'Synthetix'


def mock_redirect(requests_mock, source, target, text):
    requests_mock.get(source, status_code=302, headers={'location': target})
    requests_mock.get(target, text=text)


def test_snx_contract_address_mainnet(requests_mock):
    mock_redirect(
        requests_mock,
        source='https://contracts.synthetix.io/Synthetix',
        target='https://etherscan.io/address/0x08F30Ecf2C15A783083ab9D5b9211c22388d0564',
        text='',
    )

    assert (
        snx_contract_address(contract_name)
        == '0x08F30Ecf2C15A783083ab9D5b9211c22388d0564'
    )


def test_snx_contract_address_optimism(requests_mock):
    text = read_file('synthetix/data/contracts.md')
    requests_mock.get(
        'https://raw.githubusercontent.com/Synthetixio/synthetix-docs/master/content/addresses.md',
        text=text,
    )

    assert (
        snx_contract_address(contract_name, 'optimism')
        == '0x49B35BE7D96888C02F342552aB218d859599aCeb'
    )


def test_invalid_contract_raises(requests_mock):
    requests_mock.get('https://contracts.synthetix.io/abc', status_code=404)

    with pytest.raises(ValueError, match='Contract abc not found'):
        snx_contract_address('abc')


def test_invalid_contract_optimism_raises(requests_mock):
    text = read_file('synthetix/data/contracts.md')
    requests_mock.get(
        'https://raw.githubusercontent.com/Synthetixio/synthetix-docs/master/content/addresses.md',
        text=text,
    )

    with pytest.raises(ValueError, match='Contract abc not found'):
        snx_contract_address('abc', 'optimism')


def test_create_with_custom_api():
    api = SynthetixMainnetApi(api_url='http://localhost:1234/')
    assert api.w3.provider.endpoint_uri == 'http://localhost:1234/'


def test_create_with_custom_optimism_api():
    api = SynthetixOptimismApi(api_url='http://localhost:1234/')
    assert api.w3.provider.endpoint_uri == 'http://localhost:1234/'


@pytest.mark.skip("For some reason VCR cassette doesn't work properly")
@pytest.mark.vcr()
def test_synthetix_optimism_api():
    api = SynthetixOptimismApi(api_url='https://mainnet.optimism.io/')
    balances = api.get_balance(test_address)

    assert balances == [
        BalanceItem(
            balance=Decimal('376576.311381339269627458'),
            balance_raw=Decimal('376576311381339269627458'),
            raw={},
            coin=Coin(
                symbol='sUSD',
                name='sUSD',
                decimals=18,
                blockchain=Blockchain.OPTIMISM,
                address='0x8c6f28f2F1A3C87F0f938b96d27520d9751ec8d9',
                standards=None,
                protocol_id=None,
                info=None,
            ),
            asset_type=AssetType.DEBT,
        ),
        BalanceItem(
            balance=Decimal('528051.112125559541484602'),
            balance_raw=Decimal('528051112125559541484602'),
            raw={},
            coin=Coin(
                symbol='SNX',
                name='SNX',
                decimals=18,
                blockchain=Blockchain.OPTIMISM,
                address='0x8700dAec35aF8Ff88c16BdF0418774CB3D7599B4',
                standards=None,
                protocol_id=None,
                info=None,
            ),
            asset_type=AssetType.STAKED,
        ),
        BalanceItem(
            balance=Decimal('188153.171065910534455462'),
            balance_raw=Decimal('188153171065910534455462'),
            raw={},
            coin=Coin(
                symbol='SNX',
                name='SNX',
                decimals=18,
                blockchain=Blockchain.OPTIMISM,
                address='0x8700dAec35aF8Ff88c16BdF0418774CB3D7599B4',
                standards=None,
                protocol_id=None,
                info=None,
            ),
            asset_type=AssetType.VESTING,
        ),
    ]


@pytest.fixture()
def mocked_get_synth_contract():
    with patch(
        'blockapi.v2.api.synthetix.synthetix.SynthetixApi._get_synth_contract'
    ) as patched:
        patched.return_value = '0x0000000000000000000000000000000000000000'
        yield patched


def test_yield_balances_from_staking(mocked_get_synth_contract):
    api = SynthetixMainnetApi(api_url='http://localhost:1234/')
    staking = {
        'transferable': Decimal(10),
        'debt': Decimal(10),
        'staked': Decimal(10),
        'vesting': Decimal(8),
        'collateral': Decimal(100),
        'rewards': {
            'exchange': Decimal(2),
            'staking': Decimal(3),
        },
        'liquidation_reward': Decimal(3),
    }

    balances = list(api.yield_balances_from_staking(staking))

    assert balances[2].asset_type == AssetType.STAKED
    assert balances[2].balance_raw == Decimal(89)

    assert balances[3].asset_type == AssetType.PRICED_VESTING
    assert balances[3].balance_raw == Decimal(8)
