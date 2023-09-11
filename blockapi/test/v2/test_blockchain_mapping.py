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
        ('aptos', Blockchain.APTOS),
        ('base', Blockchain.BASE),
        ('bitkub-chain', Blockchain.BITKUB_CHAIN),
        ('bittorrent', Blockchain.BIT_TORRENT),
        ('callisto', Blockchain.CALLISTO),
        ('core', Blockchain.CORE_CHAIN),
        ('defi-kingdoms-blockchain', Blockchain.DEFI_KINGDOMS),
        ('empire', Blockchain.EMPIRE),
        ('eos-evm', Blockchain.EOS),
        ('exosama', Blockchain.EXOSAMA),
        ('flare-network', Blockchain.FLARE),
        ('function-x', Blockchain.FUNCTION_X),
        ('hoo', Blockchain.HOO_SMART_CHAIN),
        ('kujira', Blockchain.KUJIRA),
        ('linea', Blockchain.LINEA),
        ('mantle', Blockchain.MANTLE),
        ('neon-evm', Blockchain.NEON_EVM),
        ('oasis', Blockchain.OASIS_CHAIN),
        ('oasys', Blockchain.OASYS),
        ('onus', Blockchain.ONUS_CHAIN),
        ('opbnb', Blockchain.OPTIMISTIC_BNB),
        ('ordinals', Blockchain.ORDINALS),
        ('polygon-zkevm', Blockchain.POLYGON_ZK_EVM),
        ('proof-of-memes', Blockchain.PROOF_OF_MEMES),
        ('pulsechain', Blockchain.PULSE),
        ('rollux', Blockchain.ROLLUX),
        ('shibarium', Blockchain.SHIBARIUM),
        ('sui', Blockchain.SUI),
        ('tenet', Blockchain.TENET),
        ('terra-2', Blockchain.TERRA_2),
        ('the-open-network', Blockchain.OPEN_NETWORK),
        ('trustless-computer', Blockchain.TRUSTLESS_COMPUTER),
        ('wemix-network', Blockchain.WEMIX_NETWORK),
        ('zksync', Blockchain.ZKSYNC_ERA),
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
