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
        ('ailayer', Blockchain.AI_LAYER),
        ('alot', Blockchain.DEX_ALOT),
        ('apex', Blockchain.PROOF_OF_PLAY_APEX),
        ('aze', Blockchain.ASTAR_ZKEVM),
        ('b2', Blockchain.B2),
        ('bb', Blockchain.BOUNCE_BIT),
        ('bevm', Blockchain.BEVM),
        ('bfc', Blockchain.BIFROST),
        ('bob', Blockchain.BOB),
        ('brise', Blockchain.BITGERT),
        ('btr', Blockchain.BIT_LAYER),
        ('cfx', Blockchain.CONFLUX),
        ('ckb', Blockchain.GODWOKEN),
        ('degen', Blockchain.DEGEN),
        ('doge', Blockchain.DOGECHAIN),
        ('dym', Blockchain.DYMENSION),
        ('ela', Blockchain.ELASTOS),
        ('eon', Blockchain.HORIZEN_EON),
        ('era', Blockchain.ZKSYNC_ERA),
        ('fon', Blockchain.FON_CHAIN),
        ('frax', Blockchain.FRAXTAL),
        ('fx', Blockchain.FUNCTION_X),
        ('karak', Blockchain.KARAK),
        ('kroma', Blockchain.KROMA),
        ('lumio', Blockchain.SUPER_LUMIO),
        ('mada', Blockchain.MILKOMEDA_C1),
        ('manta', Blockchain.MANTA_PACIFIC),
        ('map', Blockchain.MAP_PROTOCOL),
        ('merlin', Blockchain.MERLIN_CHAIN),
        ('molten', Blockchain.MOLTEN),
        ('neon', Blockchain.NEON_EVM),
        ('nova', Blockchain.ARBITRUM_NOVA),
        ('platon', Blockchain.PLAT_ON),
        ('pze', Blockchain.POLYGON_ZK_EVM),
        ('reya', Blockchain.REYA),
        ('rsk', Blockchain.RSK),
        ('savm', Blockchain.SATOSHI_VM_ALPHA),
        ('scrl', Blockchain.SCROLL),
        ('shib', Blockchain.SHIBARIUM),
        ('step', Blockchain.STEP_NETWORK),
        ('sx', Blockchain.SX_NETWORK),
        ('taiko', Blockchain.TAIKO),
        ('tomb', Blockchain.TOMBCHAIN),
        ('ulx', Blockchain.ULTRON),
        ('xlayer', Blockchain.X_LAYER),
        ('zeta', Blockchain.ZETA_CHAIN),
        ('zklink', Blockchain.ZKLINK_NOVA),
    ],
)
def test_map_debank(chain: str, expected: Blockchain):
    assert get_blockchain_from_debank_chain(chain) == expected
