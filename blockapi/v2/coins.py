from .models import Blockchain, Coin, CoinInfo

coin_eth = Coin(
    symbol='ETH',
    name='Ethereum',
    decimals=18,
    blockchain=Blockchain.ETHEREUM,
    address='0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
    info=CoinInfo(coingecko_id='ethereum')
)
