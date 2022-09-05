from blockapi.v2.models import AssetType, Blockchain

from blockapi.v2.coins import (
    COIN_ASTR,
    COIN_AURORA,
    COIN_AVAX,
    COIN_BNB,
    COIN_BOBA,
    COIN_BTT,
    COIN_CELO,
    COIN_CRO,
    COIN_ETH,
    COIN_FTM,
    COIN_FUSE,
    COIN_GLMR,
    COIN_IOTX,
    COIN_KCS,
    COIN_KLAY,
    COIN_MATIC,
    COIN_METIS,
    COIN_MOVR,
    COIN_OKT,
    COIN_ONE,
    COIN_OP,
    COIN_RSK,
    COIN_SGB,
    COIN_TLOS,
    COIN_WAN,
    COIN_XDAI,
)


DEBANK_BLOCKCHAIN = {
    'arb': Blockchain.ARBITRUM,
    'avax': Blockchain.AVALANCHE,
    'bsc': Blockchain.BINANCE_SMART_CHAIN,
    'btt': Blockchain.BIT_TORRENT,
    'cro': Blockchain.CRONOS,
    'dfk': Blockchain.DEFI_KINGDOMS,
    'eth': Blockchain.ETHEREUM,
    'evmos': Blockchain.COSMOS,
    'ftm': Blockchain.FANTOM,
    'hmy': Blockchain.HARMONY,
    'iotx': Blockchain.IOTEX,
    'kcc': Blockchain.KU_COIN,
    'klay': Blockchain.KLAYTN,
    'matic': Blockchain.POLYGON,
    'movr': Blockchain.MOONRIVER,
    'mobm': Blockchain.MOONBEAM,
    'op': Blockchain.OPTIMISM,
    'sbch': Blockchain.SMART_BITCOIN_CASH,
    'sdn': Blockchain.SHIDEN,
    'sgb': Blockchain.SONGBIRD,
    'tlos': Blockchain.TELOS,
    'wan': Blockchain.WANCHAIN,
}

DEBANK_ASSET_TYPES = {
    'vested': AssetType.VESTING,
    'liquidity pool': AssetType.LIQUIDITY_POOL,
}

REWARD_ASSET_TYPE_MAP = {
    AssetType.LENDING: AssetType.LENDING_REWARD,
    AssetType.STAKED: AssetType.REWARDS,
    AssetType.FARMING: AssetType.REWARDS,
    AssetType.YIELD: AssetType.REWARDS,
}


NATIVE_COIN_MAP = {
    'astar': COIN_ASTR,
    'avax': COIN_AVAX,
    'aurora': COIN_AURORA,
    'bsc': COIN_BNB,
    'boba': COIN_BOBA,
    'btt': COIN_BTT,
    'celo': COIN_CELO,
    'cro': COIN_CRO,
    'eth': COIN_ETH,
    'ftm': COIN_FTM,
    'fuse': COIN_FUSE,
    'hmy': COIN_ONE,
    'iotex': COIN_IOTX,
    'kcc': COIN_KCS,
    'klay': COIN_KLAY,
    'matic': COIN_MATIC,
    'metis': COIN_METIS,
    'mobm': COIN_GLMR,
    'movr': COIN_MOVR,
    'okt': COIN_OKT,
    'op': COIN_OP,
    'rsk': COIN_RSK,
    'sgb': COIN_SGB,
    'xdai': COIN_XDAI,
    'tlos': COIN_TLOS,
    'wan': COIN_WAN,
}