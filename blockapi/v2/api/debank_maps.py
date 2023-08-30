# noinspection PyUnresolvedReferences
from blockapi.v2.coins import *
from blockapi.v2.models import (
    AssetType,
    Blockchain,
    Coin,
    CoingeckoId,
    CoingeckoMapping,
)

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

ALL_COINS = [
    var
    for var_name, var in globals().items()
    if isinstance(var, Coin) and var_name.startswith("COIN_")
]

NATIVE_COIN_MAP: dict[tuple[Blockchain, CoingeckoId], Coin] = {
    (coin.blockchain, coin.info.coingecko_id): coin
    for coin in ALL_COINS
    if coin.info and coin.info.coingecko_id
}

COINGECKO_IDS_BY_CONTRACTS: list[CoingeckoMapping] = [
    CoingeckoMapping(
        symbol='ETH',
        coingecko_id=CoingeckoId.ETHEREUM,
        contracts={
            'arb',
            'aurora',
            'base',
            'boba',
            'era',
            'etc',
            'eth',
            'linea',
            'nova',
            'op',
            'pze',
            'zora',
        },
    ),
    CoingeckoMapping(
        symbol='AURORA', coingecko_id=CoingeckoId.AURORA, contracts={'aurora'}
    ),
    CoingeckoMapping(
        symbol='AETH', coingecko_id=CoingeckoId.WETH, contracts={'aurora'}
    ),
    CoingeckoMapping(
        symbol='ASTR', coingecko_id=CoingeckoId.ASTAR, contracts={'astar'}
    ),
    CoingeckoMapping(
        symbol='AVAX', coingecko_id=CoingeckoId.AVALANCHE, contracts={'avax'}
    ),
    CoingeckoMapping(
        symbol='BNB', coingecko_id=CoingeckoId.BINANCE, contracts={'bsc', 'opbnb'}
    ),
    CoingeckoMapping(symbol='BOBA', coingecko_id=CoingeckoId.BOBA, contracts={'boba'}),
    CoingeckoMapping(
        symbol='BTT', coingecko_id=CoingeckoId.BIT_TORRENT, contracts={'btt'}
    ),
    CoingeckoMapping(
        symbol='CANTO', coingecko_id=CoingeckoId.CANTO, contracts={'canto'}
    ),
    CoingeckoMapping(symbol='CELO', coingecko_id=CoingeckoId.CELO, contracts={'celo'}),
    CoingeckoMapping(symbol='CRO', coingecko_id=CoingeckoId.CRONOS, contracts={'cro'}),
    CoingeckoMapping(symbol='FTM', coingecko_id=CoingeckoId.FANTOM, contracts={'ftm'}),
    CoingeckoMapping(symbol='FUSE', coingecko_id=CoingeckoId.FUSE, contracts={'fuse'}),
    CoingeckoMapping(symbol='ONE', coingecko_id=CoingeckoId.HARMONY, contracts={'hmy'}),
    CoingeckoMapping(
        symbol='IOTX', coingecko_id=CoingeckoId.IOTEX, contracts={'iotex'}
    ),
    CoingeckoMapping(symbol='KCS', coingecko_id=CoingeckoId.KUCOIN, contracts={'kcc'}),
    CoingeckoMapping(symbol='KLAY', coingecko_id=CoingeckoId.KLAY, contracts={'klay'}),
    CoingeckoMapping(
        symbol='MATIC', coingecko_id=CoingeckoId.MATIC, contracts={'matic'}
    ),
    CoingeckoMapping(
        symbol='METIS', coingecko_id=CoingeckoId.METIS, contracts={'metis'}
    ),
    CoingeckoMapping(
        symbol='GLMR', coingecko_id=CoingeckoId.MOONBEAM, contracts={'mobm'}
    ),
    CoingeckoMapping(
        symbol='MOVR', coingecko_id=CoingeckoId.MOONBEAM_MOONRIVER, contracts={'movr'}
    ),
    CoingeckoMapping(symbol='OKT', coingecko_id=CoingeckoId.OKT, contracts={'okt'}),
    CoingeckoMapping(symbol='OP', coingecko_id=CoingeckoId.OPTIMISM, contracts={'op'}),
    CoingeckoMapping(
        symbol='PERP', coingecko_id=CoingeckoId.PERPETUAL, contracts={'eth'}
    ),
    CoingeckoMapping(symbol='RON', coingecko_id=CoingeckoId.RONIN, contracts={'ron'}),
    CoingeckoMapping(symbol='RBTC', coingecko_id=CoingeckoId.RSK, contracts={'rsk'}),
    CoingeckoMapping(
        symbol='SGB', coingecko_id=CoingeckoId.SONGBIRD, contracts={'sgb'}
    ),
    CoingeckoMapping(symbol='XDAI', coingecko_id=CoingeckoId.XDAI, contracts={'xdai'}),
    CoingeckoMapping(symbol='TLOS', coingecko_id=CoingeckoId.TELOS, contracts={'tlos'}),
    CoingeckoMapping(
        symbol='WAN', coingecko_id=CoingeckoId.WANCHAIN, contracts={'wan'}
    ),
]
