from decimal import Decimal

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
    text = read_file('synthetix/data/contract-optimism.html')
    requests_mock.get('https://docs.synthetix.io/addresses/', text=text)

    assert (
        snx_contract_address(contract_name, 'optimism')
        == '0xFE8E48Bf36ccC3254081eC8C65965D1c8b2E744D'
    )


def test_invalid_contract_raises(requests_mock):
    requests_mock.get('https://contracts.synthetix.io/abc', status_code=404)

    with pytest.raises(ValueError, match='Contract abc not found'):
        snx_contract_address('abc')


def test_invalid_contract_optimism_raises(requests_mock):
    text = read_file('synthetix/data/contract-optimism.html')
    requests_mock.get('https://docs.synthetix.io/addresses/', text=text)

    with pytest.raises(ValueError, match='Contract abc not found'):
        snx_contract_address('abc', 'optimism')


def test_create_with_custom_api():
    api = SynthetixMainnetApi(api_url='http://localhost:1234/')
    assert api.w3.provider.endpoint_uri == 'http://localhost:1234/'


def test_create_with_custom_optimism_api():
    api = SynthetixOptimismApi(api_url='http://localhost:1234/')
    assert api.w3.provider.endpoint_uri == 'http://localhost:1234/'


@pytest.mark.vcr()
def test_synthetix_optimism_api():
    api = SynthetixOptimismApi(api_url='https://mainnet.optimism.io')
    balances = api.get_balance(test_address)

    assert balances == [
        BalanceItem(
            balance=Decimal('99738.633668060675890591'),
            balance_raw=Decimal('99738633668060675890591'),
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
            balance=Decimal('146586.533956304251544616'),
            balance_raw=Decimal('146586533956304251544616'),
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
            balance=Decimal('146382.890898962327843658'),
            balance_raw=Decimal('146382890898962327843658'),
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
