import logging
from typing import Optional, Union

from blockapi.v2.models import Blockchain

logger = logging.getLogger(__name__)

DEBANK_BLOCKCHAINS_MAP = {
    'alot': Blockchain.DEX_ALOT,
    'arb': Blockchain.ARBITRUM,
    'avax': Blockchain.AVALANCHE,
    'bfc': Blockchain.BIFROST,
    'boba': Blockchain.BOBA,
    'brise': Blockchain.BITGERT,
    'bsc': Blockchain.BINANCE_SMART_CHAIN,
    'btt': Blockchain.BIT_TORRENT,
    'cfx': Blockchain.CONFLUX,
    'ckb': Blockchain.GODWOKEN,
    'core': Blockchain.CORE_CHAIN,
    'cro': Blockchain.CRONOS,
    'dfk': Blockchain.DEFI_KINGDOMS,
    'doge': Blockchain.DOGECHAIN,
    'dym': Blockchain.DYMENSION,
    'eon': Blockchain.HORIZEN_EON,
    'era': Blockchain.ZKSYNC_ERA,
    'etc': Blockchain.ETHEREUM_CLASSIC,
    'eth': Blockchain.ETHEREUM,
    'evmos': Blockchain.COSMOS,
    'flr': Blockchain.FLARE,
    'fon': Blockchain.FON_CHAIN,
    'fsn': Blockchain.FUSION_NETWORK,
    'ftm': Blockchain.FANTOM,
    'fx': Blockchain.FUNCTION_X,
    'hmy': Blockchain.HARMONY,
    'iotx': Blockchain.IOTEX,
    'kcc': Blockchain.KUCOIN,
    'klay': Blockchain.KLAY_TOKEN,
    'lyx': Blockchain.LUKSO,
    'mada': Blockchain.MILKOMEDA_C1,
    'manta': Blockchain.MANTA_PACIFIC,
    'matic': Blockchain.POLYGON,
    'merlin': Blockchain.MERLIN_CHAIN,
    'metis': Blockchain.METIS_ANDROMEDA,
    'mnt': Blockchain.MANTLE,
    'mobm': Blockchain.MOONBEAM,
    'movr': Blockchain.MOONRIVER,
    'mtr': Blockchain.METER,
    'nova': Blockchain.ARBITRUM_NOVA,
    'oas': Blockchain.OASYS,
    'op': Blockchain.OPTIMISM,
    'opbnb': Blockchain.OPTIMISTIC_BNB,
    'pls': Blockchain.PULSE,
    'pze': Blockchain.POLYGON_ZK_EVM,
    'ron': Blockchain.RONIN,
    'rose': Blockchain.OASIS_EMERALD,
    'sbch': Blockchain.SMART_BITCOIN_CASH,
    'scrl': Blockchain.SCROLL,
    'sdn': Blockchain.SHIDEN_NETWORK,
    'sgb': Blockchain.SONGBIRD,
    'shib': Blockchain.SHIBARIUM,
    'step': Blockchain.STEP_NETWORK,
    'tlos': Blockchain.TELOS,
    'tomb': Blockchain.TOMBCHAIN,
    'wan': Blockchain.WANCHAIN,
    'wemix': Blockchain.WEMIX_NETWORK,
    'zeta': Blockchain.ZETA_CHAIN,
}

COINGECKO_BLOCKCHAINS_MAP = {
    'bittorrent': Blockchain.BIT_TORRENT,
    'core': Blockchain.CORE_CHAIN,
    'defi-kingdom-blockchain': Blockchain.DEFI_KINGDOMS,
    'defi-kingdoms-blockchain': Blockchain.DEFI_KINGDOMS,
    'eos-evm': Blockchain.EOS,
    'flare-network': Blockchain.FLARE,
    'harmony-shard-0': Blockchain.HARMONY,
    'hoo': Blockchain.HOO_SMART_CHAIN,
    'kucoin-community-chain': Blockchain.KUCOIN,
    'oasis': Blockchain.OASIS_CHAIN,
    'oec': Blockchain.OKT,
    'onus': Blockchain.ONUS_CHAIN,
    'opbnb': Blockchain.OPTIMISTIC_BNB,
    'polygon-pos': Blockchain.POLYGON,
    'pulsechain': Blockchain.PULSE,
    'shibchain': Blockchain.SHIBA_CHAIN,
    'shiden network': Blockchain.SHIDEN_NETWORK,
    'smartbch': Blockchain.SMART_BITCOIN_CASH,
    'the-open-network': Blockchain.OPEN_NETWORK,
    'thorchain': Blockchain.THOR,
    'zksync': Blockchain.ZKSYNC_ERA,
}

CHAIN_ID_BLOCKCHAINS_MAP = {
    '1': Blockchain.ETHEREUM,
    '2': Blockchain.EXPANSE_NETWORK,
    '3': None,  # testnet - Ropsten
    '4': None,  # testnet,
    '5': None,  # testnet,
    '6': None,  # testnet - Ethereum Classic Testnet Kotti
    '7': Blockchain.THAI_CHAIN,
    '8': Blockchain.UBIQ,
    '10': Blockchain.OPTIMISM,
    '12': None,  # testnet - Metadium Testnet
    '14': Blockchain.FLARE,
    '16': None,  # testnet - Flare Testnet Coston
    '17': Blockchain.THAI_CHAIN_2_THAI_FI,
    '19': Blockchain.SONGBIRD,
    '20': Blockchain.ELASTOS,
    '21': None,  # testnet - ELA-ETH-Sidechain Testnet
    '22': Blockchain.ELA_DID_SIDECHAIN,
    '23': None,  # testnet - ELA-DID-Sidechain Testnet
    '24': Blockchain.DITHEREUM,
    '25': Blockchain.CRONOS,
    '26': None,  # testnet - Genesis L1 testnet
    '27': Blockchain.SHIBA_CHAIN,
    '28': None,  # testnet
    '29': Blockchain.GENESIS_L1,
    '30': Blockchain.ROOTSTOCK,
    '31': None,  # testnet - rsk
    '32': None,  # testnet - good data
    '35': Blockchain.TBWG_CHAIN,
    '36': Blockchain.DXCHAIN,
    '37': Blockchain.SEED_COIN_NETWORK,
    '38': Blockchain.VALORBIT,
    '40': Blockchain.TELOS,
    '44': Blockchain.DARWINIA_CRAB_NETWORK,
    '56': Blockchain.BINANCE_SMART_CHAIN,
    '57': Blockchain.SYSCOIN,
    '58': Blockchain.ONTOLOGY,
    '61': Blockchain.ETHEREUM_CLASSIC,
    '66': Blockchain.OKT,
    '69': None,  # testnet
    '97': None,  # testnet
    '100': Blockchain.GNOSIS,
    '106': Blockchain.VELAS,
    '122': Blockchain.FUSE,
    '128': Blockchain.HUOBI_TOKEN,
    '137': Blockchain.POLYGON,
    '250': Blockchain.FANTOM,
    '256': None,  # testnet
    '288': Blockchain.BOBA,
    '321': Blockchain.KCC,
    '336': Blockchain.SHIDEN_NETWORK,
    '416': Blockchain.SX_NETWORK,
    '592': Blockchain.ASTAR,
    '1024': Blockchain.CLV_PARACHAIN,
    '1030': Blockchain.CONFLUX,
    '1088': Blockchain.METIS_ANDROMEDA,
    '1284': Blockchain.MOONBEAM,
    '1285': Blockchain.MOONRIVER,
    '2000': Blockchain.DOGECHAIN,
    '2001': Blockchain.MILKOMEDA_C1,
    '2222': Blockchain.KAVA,
    '4689': Blockchain.IOTEX,
    '8217': Blockchain.KLAYTN_CYPRESS,
    '9001': Blockchain.EVMOS,
    # "16350": None, #TODO: Not found
    '32659': Blockchain.FUSION_NETWORK,
    '42161': Blockchain.ARBITRUM,
    '42170': Blockchain.ARBITRUM_NOVA,
    '42220': Blockchain.CELO,
    '42262': Blockchain.EMERALD_PARATIME,
    '43114': Blockchain.AVALANCHE,
    '47805': Blockchain.REI_NETWORK,
    '53935': Blockchain.DFK_CHAIN,
    '71402': Blockchain.GODWOKEN,
    # "73772":None, #TODO: not found
    '210425': Blockchain.PLAT_ON,
    '256256': Blockchain.CMP,
    # "12340001": None, #TODO: not found
    '1313161554': Blockchain.AURORA,
    '1666600000': Blockchain.HARMONY,
}

RANGO_BLOCKCHAINS_MAP = {
    'avax_cchain': Blockchain.AVALANCHE,
    'bnb': Blockchain.BINANCECOIN,
    'bsc': Blockchain.BINANCE_SMART_CHAIN,
    'btc': Blockchain.BITCOIN,
    'crypto_org': Blockchain.CRYPTO_ORG,
    'doge': Blockchain.DOGECHAIN,
    'eth': Blockchain.ETHEREUM,
    'ltc': Blockchain.LITECOIN,
}

WORMHOLE_BLOCKCHAINS_MAP = {
    'eth': Blockchain.ETHEREUM,
    'sol': Blockchain.SOLANA,
    'bsc': Blockchain.BINANCE_SMART_CHAIN,
    'matic': Blockchain.POLYGON,
    'avax': Blockchain.AVALANCHE,
    'ftm': Blockchain.FANTOM,
}


def _get_chain_mapping(
    chain: Optional[Union[str, int]], source: str, mapping: dict[str, Blockchain]
) -> Optional[Blockchain]:
    if not chain:
        return None

    chain_lower = chain.lower() if hasattr(chain, 'lower') else str(chain)

    blockchain = mapping.get(chain_lower)
    if blockchain:
        return blockchain

    if chain_lower in Blockchain.__members__.values():
        return Blockchain(chain_lower)

    logger.warning(f'Cannot convert chain id "{chain}" to Blockchain for {source}')
    return None


def get_blockchain_from_debank_chain(chain: Optional[str]) -> Optional[Blockchain]:
    return _get_chain_mapping(chain, 'DeBank', DEBANK_BLOCKCHAINS_MAP)


def get_blockchain_from_coingecko_chain(chain: Optional[str]) -> Optional[Blockchain]:
    return _get_chain_mapping(chain, 'CoinGecko', COINGECKO_BLOCKCHAINS_MAP)


def get_blockchain_from_chain_id(
    chain: Optional[Union[str, int]]
) -> Optional[Blockchain]:
    return _get_chain_mapping(chain, 'Chain ID', CHAIN_ID_BLOCKCHAINS_MAP)


def get_blockchain_from_rango_chain(chain: Optional[str]) -> Optional[Blockchain]:
    return _get_chain_mapping(chain, 'Rango', RANGO_BLOCKCHAINS_MAP)


def get_blockchain_from_wormhole_chain(chain: Optional[str]) -> Optional[Blockchain]:
    return _get_chain_mapping(chain, 'Wormhole', WORMHOLE_BLOCKCHAINS_MAP)
