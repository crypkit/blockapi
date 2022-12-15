import pytest

from blockapi.v2.blockchain_mapping import (
    get_blockchain_from_chain_id,
    get_blockchain_from_coingecko_chain,
    get_blockchain_from_rango_chain,
)
from blockapi.v2.models import Blockchain


def test_map_case():
    assert get_blockchain_from_rango_chain('TERRA') == Blockchain.TERRA


def test_map_none():
    assert not get_blockchain_from_rango_chain(None)


@pytest.mark.parametrize(
    'chain,expected',
    [
        ('ShibChain', Blockchain.SHIBA_CHAIN),
        ('defi-kingdoms-blockchain', Blockchain.DEFI_KINGDOMS),
    ],
)
def test_map_coingecko(chain: str, expected: Blockchain):
    assert get_blockchain_from_coingecko_chain(chain) == expected


def test_map_by_id():
    assert get_blockchain_from_chain_id(1) == Blockchain.ETHEREUM
