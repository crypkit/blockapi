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
    address='So11111111111111111111111111111111111111112',
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
        coingecko_id='polygon',
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
        coingecko_id='avalanche',
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
    decimals=8,
    blockchain=Blockchain.BINANCE_SMART_CHAIN,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(
        coingecko_id='binance-coin',
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
    blockchain=Blockchain.KLAYTN,
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
    address='0x0000000000000000000000000000000000000000',
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
    blockchain=Blockchain.RSK,
    address='0x0000000000000000000000000000000000000000',
)
