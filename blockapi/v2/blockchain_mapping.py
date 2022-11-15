import logging
from typing import Optional

from blockapi.v2.models import Blockchain

logger = logging.getLogger(__name__)

DEBANK_BLOCKCHAINS = {
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

COINGECKO_BLOCKCHAINS = {}


def _get_chain_mapping(
    chain: str, source: str, mapping: dict[str, Blockchain]
) -> Optional[Blockchain]:
    try:
        blockchain = mapping.get(chain)
        if blockchain:
            return blockchain

        return Blockchain(chain)
    except ValueError:
        if logger:
            logger.warning(
                f'Cannot convert chain id "{chain}" to Blockchain for {source}'
            )

        return None


def get_blockchain_from_debank_chain(chain: str) -> Optional[Blockchain]:
    return _get_chain_mapping(chain, 'DeBank', DEBANK_BLOCKCHAINS)


def get_blockchain_from_coingecko_chain(chain: str) -> Optional[Blockchain]:
    return _get_chain_mapping(chain, 'CoinGecko', COINGECKO_BLOCKCHAINS)
