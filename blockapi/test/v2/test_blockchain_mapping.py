import pytest

from blockapi.v2.blockchain_mapping import (
    get_blockchain_from_chain_id,
    get_blockchain_from_coingecko_chain,
    get_blockchain_from_debank_chain,
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
        ('polygon-zkevm', Blockchain.POLYGON_ZK_EVM),
        ('bitkub-chain', Blockchain.BITKUB_CHAIN),
        ('proof-of-memes', Blockchain.PROOF_OF_MEMES),
        ('bittorrent', Blockchain.BIT_TORRENT),
        ('flare-network', Blockchain.FLARE),
        ('aptos', Blockchain.APTOS),
        ('onus', Blockchain.ONUS_CHAIN),
        ('core', Blockchain.CORE_CHAIN),
        ('terra-2', Blockchain.TERRA_2),
        ('zksync', Blockchain.ZKSYNC_ERA),
        ('empire', Blockchain.EMPIRE),
        ('exosama', Blockchain.EXOSAMA),
        ('hoo', Blockchain.HOO_SMART_CHAIN),
        ('function-x', Blockchain.FUNCTION_X),
        ('oasys', Blockchain.OASYS),
        ('oasis', Blockchain.OASIS_CHAIN),
        ('wemix-network', Blockchain.WEMIX_NETWORK),
    ],
)
def test_map_coingecko(chain: str, expected: Blockchain):
    assert get_blockchain_from_coingecko_chain(chain) == expected


def test_map_by_id():
    assert get_blockchain_from_chain_id(1) == Blockchain.ETHEREUM


@pytest.mark.parametrize(
    'chain,expected',
    [
        ('brise', Blockchain.BITGERT),
        ('cfx', Blockchain.CONFLUX),
        ('ckb', Blockchain.GODWOKEN),
        ('doge', Blockchain.DOGECHAIN),
        ('era', Blockchain.ZKSYNC_ERA),
        ('mada', Blockchain.MILKOMEDA_C1),
        ('pze', Blockchain.POLYGON_ZK_EVM),
        ('nova', Blockchain.ARBITRUM_NOVA),
        ('rsk', Blockchain.RSK),
        ('step', Blockchain.STEP_NETWORK),
        ('tomb', Blockchain.TOMBCHAIN),
    ],
)
def test_map_debank(chain: str, expected: Blockchain):
    assert get_blockchain_from_debank_chain(chain) == expected
