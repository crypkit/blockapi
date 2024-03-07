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
        ('blast', Blockchain.BLAST),
        ('callisto', Blockchain.CALLISTO),
        ('core', Blockchain.CORE_CHAIN),
        ('defi-kingdoms-blockchain', Blockchain.DEFI_KINGDOMS),
        ('drc-20', Blockchain.DRC_20),
        ('empire', Blockchain.EMPIRE),
        ('eos-evm', Blockchain.EOS),
        ('exosama', Blockchain.EXOSAMA),
        ('flare-network', Blockchain.FLARE),
        ('fraxtal', Blockchain.FRAXTAL),
        ('function-x', Blockchain.FUNCTION_X),
        ('hoo', Blockchain.HOO_SMART_CHAIN),
        ('hypra-network', Blockchain.HYPRA_NETWORK),
        ('kadena', Blockchain.KADENA),
        ('kujira', Blockchain.KUJIRA),
        ('linea', Blockchain.LINEA),
        ('mantle', Blockchain.MANTLE),
        ('merlin-chain', Blockchain.MERLIN_CHAIN),
        ('mode', Blockchain.MODE),
        ('neon-evm', Blockchain.NEON_EVM),
        ('oasis', Blockchain.OASIS_CHAIN),
        ('oasis-sapphire', Blockchain.OASIS_SAPPHIRE),
        ('oasys', Blockchain.OASYS),
        ('omax', Blockchain.OMAX),
        ('onus', Blockchain.ONUS_CHAIN),
        ('opbnb', Blockchain.OPTIMISTIC_BNB),
        ('ordinals', Blockchain.ORDINALS),
        ('polygon-zkevm', Blockchain.POLYGON_ZK_EVM),
        ('proof-of-memes', Blockchain.PROOF_OF_MEMES),
        ('pulsechain', Blockchain.PULSE),
        ('quicksilver', Blockchain.QUICKSILVER),
        ('rollux', Blockchain.ROLLUX),
        ('sei-network', Blockchain.SEI_NETWORK),
        ('sge', Blockchain.SGE),
        ('shibarium', Blockchain.SHIBARIUM),
        ('sui', Blockchain.SUI),
        ('tenet', Blockchain.TENET),
        ('terra-2', Blockchain.TERRA_2),
        ('the-open-network', Blockchain.OPEN_NETWORK),
        ('trustless-computer', Blockchain.TRUSTLESS_COMPUTER),
        ('valobit', Blockchain.VALOBIT),
        ('wemix-network', Blockchain.WEMIX_NETWORK),
        ('xpla', Blockchain.XPLA),
        ('zetachain', Blockchain.ZETA_CHAIN),
        ('zkfair', Blockchain.ZKFAIR),
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
        ('alot', Blockchain.DEX_ALOT),
        ('bfc', Blockchain.BIFROST),
        ('brise', Blockchain.BITGERT),
        ('cfx', Blockchain.CONFLUX),
        ('ckb', Blockchain.GODWOKEN),
        ('doge', Blockchain.DOGECHAIN),
        ('dym', Blockchain.DYMENSION),
        ('eon', Blockchain.HORIZEN_EON),
        ('era', Blockchain.ZKSYNC_ERA),
        ('fon', Blockchain.FON_CHAIN),
        ('fx', Blockchain.FUNCTION_X),
        ('mada', Blockchain.MILKOMEDA_C1),
        ('manta', Blockchain.MANTA_PACIFIC),
        ('merlin', Blockchain.MERLIN_CHAIN),
        ('nova', Blockchain.ARBITRUM_NOVA),
        ('pze', Blockchain.POLYGON_ZK_EVM),
        ('rsk', Blockchain.RSK),
        ('scrl', Blockchain.SCROLL),
        ('shib', Blockchain.SHIBARIUM),
        ('step', Blockchain.STEP_NETWORK),
        ('tomb', Blockchain.TOMBCHAIN),
        ('zeta', Blockchain.ZETA_CHAIN),
    ],
)
def test_map_debank(chain: str, expected: Blockchain):
    assert get_blockchain_from_debank_chain(chain) == expected
