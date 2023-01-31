from .models import Blockchain, Coin, CoinInfo

COIN_ETH = Coin(
    symbol='ETH',
    name='Ethereum',
    decimals=18,
    blockchain=Blockchain.ETHEREUM,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(coingecko_id='ethereum'),
)


COIN_SOL = Coin(
    symbol='SOL',
    name='Solana',
    decimals=9,
    blockchain=Blockchain.SOLANA,
    info=CoinInfo(
        logo_url='https://raw.githubusercontent.com/solana-labs/token-list/main/assets/'
        'mainnet/So11111111111111111111111111111111111111112/logo.png',
        coingecko_id='solana',
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
        coingecko_id='terra-luna',
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
        coingecko_id='matic-network',
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
        coingecko_id='shiden-network',
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
        coingecko_id='avalanche-2',
        website='https://www.avax.network/',
    ),
)

COIN_RON = Coin(
    symbol='RON',
    name='Ronin',
    decimals=18,
    blockchain=Blockchain.AXIE,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(
        coingecko_id='ronin',
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
        coingecko_id='binancecoin',
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
        coingecko_id='fantom',
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
        coingecko_id='huobi-token',
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
        coingecko_id='iotex',
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
        coingecko_id='klaytn',
        website='https://www.klaytn.com/',
    ),
)

COIN_MOVR = Coin(
    symbol='MOVR',
    name='Moonriver',
    decimals=18,
    blockchain=Blockchain.MOONBEAM_MOONRIVER,
    address='0x98878b06940ae243284ca214f92bb71a2b032b8a',
    info=CoinInfo(
        coingecko_id='moonriver',
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
        coingecko_id='perpetual-protocol',
        website='https://perpetual.io/',
    ),
)


COIN_RSK = Coin(
    symbol='RBTC',
    name='Rootstock RSK',
    decimals=18,  # TODO verify this.
    blockchain=Blockchain.ROOTSTOCK,
    address='0x0000000000000000000000000000000000000000',
)

COIN_DOT = Coin(
    symbol='DOT',
    name='Polkadot',
    decimals=10,
    blockchain=Blockchain.POLKADOT,
    info=CoinInfo(coingecko_id='polkadot', tags=['native']),
)

COIN_KSM = Coin(
    symbol='KSM',
    name='Kusama',
    decimals=12,
    blockchain=Blockchain.KUSAMA,
    info=CoinInfo(coingecko_id='kusama', tags=['native']),
)

COIN_ATOM = Coin(
    symbol='ATOM',
    name='Cosmos Hub',
    decimals=6,
    blockchain=Blockchain.COSMOS,
    address='uatom',
    standards=['staking'],
    info=CoinInfo(coingecko_id='cosmos'),
)

COIN_XDAI = Coin(
    symbol='XDAI',
    name='xDai',
    decimals=18,
    blockchain=Blockchain.XDAI,
    info=CoinInfo(coingecko_id='xdai'),
)

COIN_OKT = Coin(
    symbol='OKT',
    name='OKC',
    decimals=18,
    blockchain=Blockchain.OKT,
    info=CoinInfo(coingecko_id='oec-token'),
)

COIN_OP = Coin(
    symbol='OP',
    name='OP',
    decimals=18,
    blockchain=Blockchain.OPTIMISM,
    address='0x4200000000000000000000000000000000000042',
    info=CoinInfo(coingecko_id='optimism'),
)

COIN_CELO = Coin(
    symbol='CELO',
    name='Celo',
    decimals=18,
    blockchain=Blockchain.CELO,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(coingecko_id='celo'),
)

COIN_CRO = Coin(
    symbol='CRO',
    name='Cronos',
    decimals=18,
    blockchain=Blockchain.CRONOS,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(coingecko_id='crypto-com-chain'),
)

COIN_BOBA = Coin(
    symbol='BOBA',
    name='Boba Network',
    decimals=18,
    blockchain=Blockchain.BOBA,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(coingecko_id='boba-network'),
)

COIN_METIS = Coin(
    symbol='METIS',
    name='Metis',
    decimals=18,
    blockchain=Blockchain.METIS_ANDROMEDA,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(coingecko_id='metis-token'),
)

COIN_BTT = Coin(
    symbol='BTT',
    name='BitTorrent',
    decimals=18,
    blockchain=Blockchain.BIT_TORRENT,
    address='TAFjULxiVgT4qWk6UZwjqwZXTSaGaqnVp4',
    info=CoinInfo(coingecko_id='bittorrent'),
)

COIN_AURORA = Coin(
    symbol='AURORA',
    name='Aurora',
    decimals=18,
    blockchain=Blockchain.AURORA,
    address='0xaaaaaa20d9e0e2461697782ef11675f668207961',
    info=CoinInfo(coingecko_id='aurora-near'),
)

COIN_GLMR = Coin(
    symbol='GLMR',
    name='Moonbeam',
    decimals=18,
    blockchain=Blockchain.MOONBEAM,
    info=CoinInfo(coingecko_id='moonbeam'),
)

COIN_FUSE = Coin(
    symbol='FUSE',
    name='Fuse',
    decimals=18,
    blockchain=Blockchain.FUSE,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(coingecko_id='fuse-network-token'),
)

COIN_ONE = Coin(
    symbol='ONE',
    name='Harmony',
    decimals=18,
    blockchain=Blockchain.HARMONY,
    info=CoinInfo(coingecko_id='harmony'),
)

COIN_ASTR = Coin(
    symbol='ASTR',
    name='Astar',
    decimals=18,
    blockchain=Blockchain.ASTAR,
    info=CoinInfo(coingecko_id='astar'),
)

COIN_WAN = Coin(
    symbol='WAN',
    name='Wanchain',
    decimals=18,
    blockchain=Blockchain.WANCHAIN,
    info=CoinInfo(coingecko_id='wanchain'),
)

COIN_KCS = Coin(
    symbol='KCS',
    name='KuCoin',
    decimals=18,
    blockchain=Blockchain.KUCOIN,
    info=CoinInfo(coingecko_id='kucoin-shares'),
)

COIN_SGB = Coin(
    symbol='SGB',
    name='Songbird',
    decimals=18,
    blockchain=Blockchain.SONGBIRD,
    info=CoinInfo(coingecko_id='songbird'),
)

COIN_EVMOS = Coin(
    symbol='EVMOS',
    name='EvmOS',
    decimals=18,
    blockchain=Blockchain.COSMOS,
    info=CoinInfo(coingecko_id='evmos'),
)

COIN_TLOS = Coin(
    symbol='TLOS',
    name='Telos',
    decimals=18,
    blockchain=Blockchain.TELOS,
)

COIN_BOS = Coin(symbol='BOS', name="BosCoin", decimals=7, blockchain=Blockchain.BOS)

COIN_BTC = Coin(
    symbol='BTC',
    name='Bitcoin',
    decimals=8,
    blockchain=Blockchain.BITCOIN,
    info=CoinInfo(coingecko_id='bitcoin'),
)

COIN_LTC = Coin(
    symbol='LTC',
    name='Litecoin',
    decimals=8,
    blockchain=Blockchain.LITECOIN,
    info=CoinInfo(coingecko_id='litecoin'),
)


COIN_DOGE = Coin(
    symbol='DOGE',
    name='Dogecoin',
    decimals=8,
    blockchain=Blockchain.DOGECHAIN,
    info=CoinInfo(coingecko_id='dogecoin'),
)

COIN_SNX = Coin(
    symbol='SNX',
    name='Synthetix',
    decimals=18,
    address='0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f',
    blockchain=Blockchain.ETHEREUM,
    info=CoinInfo(coingecko_id='havven'),
)
