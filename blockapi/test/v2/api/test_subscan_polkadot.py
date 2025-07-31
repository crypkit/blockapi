from decimal import Decimal

import pytest

from blockapi.test.v2.api.conftest import read_file
from blockapi.v2.api import PolkadotSubscanApi
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
        'https://polkadot.api.subscan.io/api/v2/scan/search',
        text=read_file(response_path),
    )

    balances = api.get_balance(address)
    assert sum(b.balance for b in balances) == expected_balance


def test_real_problematic_address_overlap(requests_mock, api):
    """
    Test the real problematic address that exhibits balance overlap.
    """
    requests_mock.post(
        'https://polkadot.api.subscan.io/api/v2/scan/search',
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
        'https://polkadot.api.subscan.io/api/v2/scan/search',
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
