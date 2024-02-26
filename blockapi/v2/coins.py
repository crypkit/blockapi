from .models import Blockchain, Coin, CoingeckoId, CoinInfo

COIN_ETH = Coin(
    symbol='ETH',
    name='Ethereum',
    decimals=18,
    blockchain=Blockchain.ETHEREUM,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(coingecko_id=CoingeckoId.ETHEREUM),
)

COIN_WETH = Coin(
    symbol='WETH',
    name='Wrapped Ethereum',
    decimals=18,
    blockchain=Blockchain.ETHEREUM,
    address='0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
    info=CoinInfo(coingecko_id=CoingeckoId.WETH),
)


COIN_SOL = Coin(
    symbol='SOL',
    name='Solana',
    decimals=9,
    blockchain=Blockchain.SOLANA,
    info=CoinInfo(
        logo_url='https://raw.githubusercontent.com/solana-labs/token-list/main/assets/'
        'mainnet/So11111111111111111111111111111111111111112/logo.png',
        coingecko_id=CoingeckoId.SOLANA,
        website='https://solana.com/',
    ),
)


COIN_TERRA = Coin(
    symbol='LUNA',
    name='Terra',
    decimals=6,
    blockchain=Blockchain.TERRA,
    address='uluna',
    standards=['terra-native'],
    info=CoinInfo(
        logo_url='https://assets.terra.money/icon/60/Luna.png',
        coingecko_id=CoingeckoId.LUNA,
        website='https://www.terra.money/',
    ),
)


COIN_MATIC = Coin(
    symbol='MATIC',
    name='Matic',
    decimals=18,
    blockchain=Blockchain.POLYGON,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(
        coingecko_id=CoingeckoId.MATIC,
        website='https://polygon.technology/',
    ),
)

COIN_SDN = Coin(
    symbol='SDN',
    name='Shiden Network',
    decimals=18,
    blockchain=Blockchain.ASTAR,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(
        coingecko_id=CoingeckoId.SHIDEN,
        website='https://shiden.astar.network/',
    ),
)

COIN_AVAX = Coin(
    symbol='AVAX',
    name='AVAX',
    decimals=18,
    blockchain=Blockchain.AVALANCHE,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(
        coingecko_id=CoingeckoId.AVALANCHE,
        website='https://www.avax.network/',
    ),
)

COIN_RON = Coin(
    symbol='RON',
    name='Ronin',
    decimals=18,
    blockchain=Blockchain.RONIN,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(
        coingecko_id=CoingeckoId.RONIN,
        website='https://bridge.roninchain.com',
    ),
)

COIN_AXIE_RON = Coin(
    symbol='RON',
    name='Ronin',
    decimals=18,
    blockchain=Blockchain.AXIE,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(
        coingecko_id=CoingeckoId.RONIN,
        website='https://bridge.roninchain.com',
    ),
)

COIN_BNB = Coin(
    symbol='BNB',
    name='Binance Coin',
    decimals=18,
    blockchain=Blockchain.BINANCE_SMART_CHAIN,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(
        coingecko_id=CoingeckoId.BINANCE,
        website='https://www.binance.com',
    ),
)

COIN_FTM = Coin(
    symbol='FTM',
    name='Fantom',
    decimals=18,
    blockchain=Blockchain.FANTOM,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(
        coingecko_id=CoingeckoId.FANTOM,
        website='https://fantom.foundation',
    ),
)

COIN_HT = Coin(
    symbol='HT',
    name='Huobi Token',
    decimals=18,
    blockchain=Blockchain.HECO,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(
        coingecko_id=CoingeckoId.HUOBI,
        website='https://www.huobi.com',
    ),
)

COIN_IOTX = Coin(
    symbol='IOTX',
    name='IoTeX',
    decimals=18,
    blockchain=Blockchain.IOTEX,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(
        coingecko_id=CoingeckoId.IOTEX,
        website='https://iotex.io/',
    ),
)

COIN_KLAY = Coin(
    symbol='KLAY',
    name='Klaytn',
    decimals=18,
    blockchain=Blockchain.KLAY_TOKEN,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(
        coingecko_id=CoingeckoId.KLAY,
        website='https://www.klaytn.com/',
    ),
)

COIN_MOVR = Coin(
    symbol='MOVR',
    name='Moonriver',
    decimals=18,
    blockchain=Blockchain.MOONRIVER,
    address='0x98878b06940ae243284ca214f92bb71a2b032b8a',
    info=CoinInfo(
        coingecko_id=CoingeckoId.MOONBEAM_MOONRIVER,
        website='https://moonbeam.network/networks/moonriver/',
    ),
)

COIN_PALM = Coin(
    symbol='PALM',
    name='Palm',
    decimals=18,
    blockchain=Blockchain.PALM,
    address='0x0000000000000000000000000000000000000000',
)

COIN_PERP = Coin(
    symbol='PERP',
    name='Perpetual',
    decimals=0,
    blockchain=Blockchain.ETHEREUM,
    address='0xbC396689893D065F41bc2C6EcbeE5e0085233447',
    info=CoinInfo(
        coingecko_id=CoingeckoId.PERPETUAL,
        website='https://perpetual.io/',
    ),
)

COIN_RSK = Coin(
    symbol='RBTC',
    name='Rootstock RSK',
    decimals=18,  # TODO verify this.
    blockchain=Blockchain.RSK,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(coingecko_id=CoingeckoId.RSK),
)

COIN_DOT = Coin(
    symbol='DOT',
    name='Polkadot',
    decimals=10,
    blockchain=Blockchain.POLKADOT,
    info=CoinInfo(coingecko_id=CoingeckoId.POLKADOT, tags=['native']),
)

COIN_KSM = Coin(
    symbol='KSM',
    name='Kusama',
    decimals=12,
    blockchain=Blockchain.KUSAMA,
    info=CoinInfo(coingecko_id=CoingeckoId.KUSAMA, tags=['native']),
)

COIN_ATOM = Coin(
    symbol='ATOM',
    name='Cosmos Hub',
    decimals=6,
    blockchain=Blockchain.COSMOS,
    address='uatom',
    standards=['staking'],
    info=CoinInfo(coingecko_id=CoingeckoId.COSMOS),
)

COIN_XDAI = Coin(
    symbol='XDAI',
    name='xDai',
    decimals=18,
    blockchain=Blockchain.XDAI,
    info=CoinInfo(coingecko_id=CoingeckoId.XDAI),
)

COIN_DAI = Coin(
    symbol='DAI',
    name='Dai',
    decimals=18,
    blockchain=Blockchain.ETHEREUM,
    info=CoinInfo(coingecko_id=CoingeckoId.DAI),
)

COIN_OKT = Coin(
    symbol='OKT',
    name='OKC',
    decimals=18,
    blockchain=Blockchain.OKT,
    info=CoinInfo(coingecko_id=CoingeckoId.OKT),
)

COIN_OP = Coin(
    symbol='OP',
    name='OP',
    decimals=18,
    blockchain=Blockchain.OPTIMISM,
    address='0x4200000000000000000000000000000000000042',
    info=CoinInfo(coingecko_id=CoingeckoId.OPTIMISM),
)

COIN_CELO = Coin(
    symbol='CELO',
    name='Celo',
    decimals=18,
    blockchain=Blockchain.CELO,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(coingecko_id=CoingeckoId.CELO),
)

COIN_CRO = Coin(
    symbol='CRO',
    name='Cronos',
    decimals=18,
    blockchain=Blockchain.CRONOS,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(coingecko_id=CoingeckoId.CRONOS),
)

COIN_BOBA = Coin(
    symbol='BOBA',
    name='Boba Network',
    decimals=18,
    blockchain=Blockchain.BOBA,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(coingecko_id=CoingeckoId.BOBA),
)

COIN_METIS = Coin(
    symbol='METIS',
    name='Metis',
    decimals=18,
    blockchain=Blockchain.METIS_ANDROMEDA,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(coingecko_id=CoingeckoId.METIS),
)

COIN_BTT = Coin(
    symbol='BTT',
    name='BitTorrent',
    decimals=18,
    blockchain=Blockchain.BIT_TORRENT,
    address='TAFjULxiVgT4qWk6UZwjqwZXTSaGaqnVp4',
    info=CoinInfo(coingecko_id=CoingeckoId.BIT_TORRENT),
)

COIN_AURORA = Coin(
    symbol='AURORA',
    name='Aurora',
    decimals=18,
    blockchain=Blockchain.AURORA,
    address='0xaaaaaa20d9e0e2461697782ef11675f668207961',
    info=CoinInfo(coingecko_id=CoingeckoId.AURORA),
)

COIN_AURORA_AETH = Coin(
    symbol='AETH',
    name='Wrapped Ethereum',
    decimals=18,
    blockchain=Blockchain.AURORA,
    address='0xc9bdeed33cd01541e1eed10f90519d2c06fe3feb',
    info=CoinInfo(coingecko_id=CoingeckoId.WETH),  # inconsistent: AETH <-> WETH
)

COIN_GLMR = Coin(
    symbol='GLMR',
    name='Moonbeam',
    decimals=18,
    blockchain=Blockchain.MOONBEAM,
    info=CoinInfo(coingecko_id=CoingeckoId.MOONBEAM),
)

COIN_FUSE = Coin(
    symbol='FUSE',
    name='Fuse',
    decimals=18,
    blockchain=Blockchain.FUSE,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(coingecko_id=CoingeckoId.FUSE),
)

COIN_ONE = Coin(
    symbol='ONE',
    name='Harmony',
    decimals=18,
    blockchain=Blockchain.HARMONY,
    info=CoinInfo(coingecko_id=CoingeckoId.HARMONY),
)

COIN_ASTR = Coin(
    symbol='ASTR',
    name='Astar',
    decimals=18,
    blockchain=Blockchain.ASTAR,
    info=CoinInfo(coingecko_id=CoingeckoId.ASTAR),
)

COIN_WAN = Coin(
    symbol='WAN',
    name='Wanchain',
    decimals=18,
    blockchain=Blockchain.WANCHAIN,
    info=CoinInfo(coingecko_id=CoingeckoId.WANCHAIN),
)

COIN_KCS = Coin(
    symbol='KCS',
    name='KuCoin',
    decimals=18,
    blockchain=Blockchain.KUCOIN,
    info=CoinInfo(coingecko_id=CoingeckoId.KUCOIN),
)

COIN_SGB = Coin(
    symbol='SGB',
    name='Songbird',
    decimals=18,
    blockchain=Blockchain.SONGBIRD,
    info=CoinInfo(coingecko_id=CoingeckoId.SONGBIRD),
)

COIN_EVMOS = Coin(
    symbol='EVMOS',
    name='EvmOS',
    decimals=18,
    blockchain=Blockchain.COSMOS,
    info=CoinInfo(coingecko_id=CoingeckoId.EVMOS),
)

COIN_TLOS = Coin(
    symbol='TLOS',
    name='Telos',
    decimals=18,
    blockchain=Blockchain.TELOS,
    info=CoinInfo(coingecko_id=CoingeckoId.TELOS),
)

COIN_BOS = Coin(symbol='BOS', name="BosCoin", decimals=7, blockchain=Blockchain.BOS)

COIN_BTC = Coin(
    symbol='BTC',
    name='Bitcoin',
    decimals=8,
    blockchain=Blockchain.BITCOIN,
    info=CoinInfo(coingecko_id=CoingeckoId.BITCOIN),
)

COIN_LTC = Coin(
    symbol='LTC',
    name='Litecoin',
    decimals=8,
    blockchain=Blockchain.LITECOIN,
    info=CoinInfo(coingecko_id=CoingeckoId.LITECOIN),
)


COIN_DOGE = Coin(
    symbol='DOGE',
    name='Dogecoin',
    decimals=8,
    blockchain=Blockchain.DOGECHAIN,
    info=CoinInfo(coingecko_id=CoingeckoId.DOGECOIN),
)

COIN_SNX = Coin(
    symbol='SNX',
    name='Synthetix',
    decimals=18,
    address='0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f',
    blockchain=Blockchain.ETHEREUM,
    info=CoinInfo(coingecko_id=CoingeckoId.SYNTHETIX),
)


COIN_CANTO = Coin(
    symbol='CANTO',
    name='Canto',
    decimals=18,
    blockchain=Blockchain.CANTO,
    address='0x826551890dc65655a0aceca109ab11abdbd7a07b',
    info=CoinInfo(coingecko_id=CoingeckoId.CANTO),
)

COIN_USDC = Coin(
    symbol='USDC',
    name='USDC',
    decimals=6,
    blockchain=Blockchain.ETHEREUM,
    address='0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
    info=CoinInfo(coingecko_id=CoingeckoId.USDC),
)

COIN_PRIME = Coin(
    symbol='PRIME',
    name='Echelon Prime',
    decimals=18,
    blockchain=Blockchain.ETHEREUM,
    address="0xb23d80f5fefcddaa212212f028021b41ded428cf",
    info=CoinInfo(coingecko_id=CoingeckoId.PRIME),
)


COIN_OSMOSIS = Coin(
    symbol='OSMO',
    name='Osmosis',
    decimals=6,
    blockchain=Blockchain.OSMOSIS,
    address="uosmo",
    info=CoinInfo(coingecko_id=CoingeckoId.OSMOSIS),
)

COIN_DYDX = Coin(
    symbol='DYDX',
    name='dYdX',
    decimals=18,
    blockchain=Blockchain.DYDX,
    address="adydx",
    info=CoinInfo(coingecko_id=CoingeckoId.DYDX),
)


COIN_CELESTIA = Coin(
    symbol='TIA',
    name='Celestia',
    decimals=6,
    blockchain=Blockchain.CELESTIA,
    address="utia",
    info=CoinInfo(coingecko_id=CoingeckoId.CELESTIA),
)
