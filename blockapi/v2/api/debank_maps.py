from blockapi.v2.coins import (
    COIN_ASTR,
    COIN_AURORA,
    COIN_AURORA_AETH,
    COIN_AVAX,
    COIN_BNB,
    COIN_BOBA,
    COIN_BTT,
    COIN_CANTO,
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
from blockapi.v2.models import AssetType, Blockchain, Coin

DEBANK_ASSET_TYPES = {
    'deposit': AssetType.DEPOSITED,
    'vested': AssetType.VESTING,
    'liquidity pool': AssetType.LIQUIDITY_POOL,
}

REWARD_ASSET_TYPE_MAP = {
    AssetType.LENDING: AssetType.LENDING_REWARDS,
    AssetType.STAKED: AssetType.REWARDS,
    AssetType.FARMING: AssetType.REWARDS,
    AssetType.YIELD: AssetType.REWARDS,
    AssetType.LIQUIDITY_POOL: AssetType.REWARDS,
    AssetType.LOCKED: AssetType.REWARDS,
}


NATIVE_COIN_MAP = {
    ('astar', COIN_ASTR.symbol): COIN_ASTR,
    ('avax', COIN_AVAX.symbol): COIN_AVAX,
    ('aurora', COIN_AURORA.symbol): COIN_AURORA,
    ('aurora', COIN_AURORA_AETH.symbol): COIN_AURORA_AETH,
    ('bsc', COIN_BNB.symbol): COIN_BNB,
    ('boba', COIN_BOBA.symbol): COIN_BOBA,
    ('btt', COIN_BTT.symbol): COIN_BTT,
    ('canto', COIN_CANTO.symbol): COIN_CANTO,
    ('celo', COIN_CELO.symbol): COIN_CELO,
    ('cro', COIN_CRO.symbol): COIN_CRO,
    ('eth', COIN_ETH.symbol): COIN_ETH,
    ('ftm', COIN_FTM.symbol): COIN_FTM,
    ('fuse', COIN_FUSE.symbol): COIN_FUSE,
    ('hmy', COIN_ONE.symbol): COIN_ONE,
    ('iotex', COIN_IOTX.symbol): COIN_IOTX,
    ('kcc', COIN_KCS.symbol): COIN_KCS,
    ('klay', COIN_KLAY.symbol): COIN_KLAY,
    ('matic', COIN_MATIC.symbol): COIN_MATIC,
    ('metis', COIN_METIS.symbol): COIN_METIS,
    ('mobm', COIN_GLMR.symbol): COIN_GLMR,
    ('movr', COIN_MOVR.symbol): COIN_MOVR,
    ('okt', COIN_OKT.symbol): COIN_OKT,
    ('op', COIN_OP.symbol): COIN_OP,
    ('rsk', COIN_RSK.symbol): COIN_RSK,
    ('sgb', COIN_SGB.symbol): COIN_SGB,
    ('xdai', COIN_XDAI.symbol): COIN_XDAI,
    ('tlos', COIN_TLOS.symbol): COIN_TLOS,
    ('wan', COIN_WAN.symbol): COIN_WAN,
}


ALL_COINS = {
    var.symbol.lower(): var
    for var_name, var in globals().items()
    if isinstance(var, Coin) and var_name.startswith("COIN_")
}
