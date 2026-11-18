from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api import PolkadotSubscanApi
from blockapi.v2.base import InvalidAddressException
from blockapi.v2.models import AssetType


@pytest.fixture
def api():
    """Create a PolkadotSubscanApi instance for testing."""
    return PolkadotSubscanApi()


@pytest.mark.parametrize(
    'address, response_path, expected_balance',
    [
        (
            '1NjjK81oA9is7eWhFJ7n7kQhaPT3pnxLFH5MkwDfduAiWE9',
            'data/subscan_polkadot_response_WE9.json',
            Decimal('4649.9139999889'),
        ),
        (
            '15j4dg5GzsL1bw2U2AWgeyAk6QTxq43V7ZPbXdAmbVLjvDCK',
            'data/subscan_polkadot_response_DCK.json',
            Decimal('17970279.0085871699'),
        ),
    ],
)
def test_fetch_balances(requests_mock, address, response_path, expected_balance, api):
    requests_mock.post(
        'https://assethub-polkadot.api.subscan.io/api/v2/scan/search',
        text=read_file(response_path),
    )

    balances = api.get_balance(address)
    assert sum(b.balance for b in balances) == expected_balance
    assert all(isinstance(balance.raw, dict) for balance in balances)


def test_real_problematic_address_overlap(requests_mock, api):
    """
    Test the real problematic address that exhibits balance overlap.
    """
    requests_mock.post(
        'https://assethub-polkadot.api.subscan.io/api/v2/scan/search',
        text=read_file('data/subscan_polkadot_balance_overlap_1567z.json'),
    )

    balances = list(api.get_balance("1567zYrTN6G1YXoF47KyC5Lyto8MhJjzDB8dY8ZvudMAAEet"))
    available_balances = [b for b in balances if b.asset_type == AssetType.AVAILABLE]

    assert len(available_balances) == 1, "Expected 1 available balance item"
    available_balance = available_balances[0]

    # Correct calculation: 69.1806120067 - 64.5655723106 = 4.6150396961 DOT
    expected_balance = Decimal("4.6150396961")
    assert (
        available_balance.balance == expected_balance
    ), f"Expected {expected_balance}, got {available_balance.balance}"


def test_second_problematic_address_overlap(requests_mock, api):
    """
    Test another problematic address with reserved > locked scenario.

    Address 15gT3MY2oVDqi1WPFnpkhPKVNUXAUPscMagaJeW8dqmLzfJ6 has large reserved
    amount (154.31 DOT) but no staking locks, demonstrating reserved > locked case.
    """
    requests_mock.post(
        'https://assethub-polkadot.api.subscan.io/api/v2/scan/search',
        text=read_file('data/subscan_polkadot_balance_overlap_15gT3.json'),
    )

    balances = list(api.get_balance("15gT3MY2oVDqi1WPFnpkhPKVNUXAUPscMagaJeW8dqmLzfJ6"))

    available_balances = [b for b in balances if b.asset_type == AssetType.AVAILABLE]
    assert len(available_balances) == 1
    available_balance = available_balances[0]

    # 162.469 total, 154.307 locked
    expected_balance = Decimal('8.1611794137')
    assert (
        available_balance.balance == expected_balance
    ), f"Expected {expected_balance}, got {available_balance.balance}"

    other_balances = [b for b in balances if b.asset_type != AssetType.AVAILABLE]
    assert len(other_balances) == 1

    other_balance = other_balances[0]
    assert other_balance.balance == Decimal('154.3078601187')
    assert other_balance.asset_type == AssetType.LOCKED


def test_bonded_above_reserved_does_not_overcount(requests_mock, api):
    # 15j4dg5G... on Asset Hub: staking ledger 7920963.40 > held 7920960.99
    account = {
        'balance': '7921211.1136402109',
        'reserved': '79209609960724902',
        'bonded': '79209634033624902',
    }
    requests_mock.post(
        'https://assethub-polkadot.api.subscan.io/api/v2/scan/search',
        json={'code': 0, 'data': {'account': account}},
    )

    balances = api.get_balance('15j4dg5GzsL1bw2U2AWgeyAk6QTxq43V7ZPbXdAmbVLjvDCK')

    assert {b.asset_type: b.balance for b in balances} == {
        AssetType.AVAILABLE: Decimal('250.1175677207'),
        AssetType.STAKED: Decimal('7920960.9960724902'),
    }


NOT_FOUND = {'code': 10004, 'message': 'Record Not Found', 'data': None}


def test_account_unknown_to_asset_hub_has_no_balances(requests_mock, api):
    requests_mock.post(
        'https://assethub-polkadot.api.subscan.io/api/v2/scan/search',
        json=NOT_FOUND,
    )

    assert api.get_balance('148x3evJb8aLBrpvPU3AN8cRAphjhNLiT3o12BvFyDdhL289') == []


@pytest.mark.parametrize(
    'address',
    [
        'not-an-address',
        # valid address with its last character changed: bad checksum
        '148x3evJb8aLBrpvPU3AN8cRAphjhNLiT3o12BvFyDdhL288',
    ],
)
def test_invalid_address_raises(requests_mock, api, address):
    requests_mock.post(
        'https://assethub-polkadot.api.subscan.io/api/v2/scan/search',
        json=NOT_FOUND,
    )

    with pytest.raises(InvalidAddressException):
        api.get_balance(address)
