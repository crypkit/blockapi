from blockapi.v2.coins import (
    COIN_DAI,
    COIN_ETH,
    COIN_MATIC,
    COIN_PRIME,
    COIN_USDC,
    COIN_WETH,
)
from blockapi.v2.models import Blockchain, Coin

OPENSEA_COINS: dict[str, Coin] = {
    'ETH': COIN_ETH,
    'USDC': COIN_USDC,
    'PRIME': COIN_PRIME,
    'DAI': COIN_DAI,
    'MATIC': COIN_MATIC,
}

OPENSEA_CONTRACTS = {
    ('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', Blockchain.ETHEREUM): COIN_WETH,
    ('0x0000000000000000000000000000000000000000', Blockchain.ETHEREUM): COIN_ETH,
}
