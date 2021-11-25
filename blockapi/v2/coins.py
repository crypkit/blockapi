from .models import Blockchain, Coin, CoinInfo

coin_eth = Coin(
    symbol='ETH',
    name='Ethereum',
    decimals=18,
    blockchain=Blockchain.ETHEREUM,
    address='0x0000000000000000000000000000000000000000',
    info=CoinInfo(coingecko_id='ethereum'),
)


coin_sol = Coin(
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


coin_terra = Coin(
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
