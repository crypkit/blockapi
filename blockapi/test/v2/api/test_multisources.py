import pytest

from blockapi.test.v2.test_data import btc_test_address, ltc_test_address
from blockapi.v2.api import (
    BlockchairBitcoinApi,
    BlockchairLitecoinApi,
    TrezorBitcoin1Api,
    TrezorBitcoin2Api,
    TrezorLitecoinApi,
)


@pytest.mark.integration
def test_btc_response_matches_from_multiple_sources():
    blockchair = BlockchairBitcoinApi()
    blockchair_balance = blockchair.get_balance(btc_test_address)

    trezor1 = TrezorBitcoin1Api()
    trezor1_balance = trezor1.get_balance(btc_test_address)

    trezor2 = TrezorBitcoin2Api()
    trezor2_balance = trezor2.get_balance(btc_test_address)

    assert len(trezor1_balance) == len(trezor2_balance) == len(blockchair_balance)

    for idx in range(len(trezor1_balance)):
        assert (
            trezor1_balance[idx].balance
            == trezor2_balance[idx].balance
            == blockchair_balance[idx].balance
        )


@pytest.mark.integration
def test_ltc_response_matches_from_multiple_sources():
    blockchair = BlockchairLitecoinApi()
    blockchair_balance = blockchair.get_balance(ltc_test_address)

    trezor1 = TrezorLitecoinApi()
    trezor1_balance = trezor1.get_balance(ltc_test_address)

    assert len(trezor1_balance) == len(blockchair_balance)

    for idx in range(len(trezor1_balance)):
        assert trezor1_balance[idx].balance == blockchair_balance[idx].balance
