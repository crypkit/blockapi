from blockapi.v2.api.blockchainos import BlockchainosApi
from blockapi.v2.api.blockchair import BlockchairBitcoinApi
from blockapi.v2.api.debank import DebankApi
from blockapi.v2.api.ethplorer import EthplorerApi
from blockapi.v2.api.optimistic_etherscan import OptimismEtherscanApi
from blockapi.v2.api.perpetual import PerpetualApi
from blockapi.v2.api.solana import SolanaApi, SolscanApi
from blockapi.v2.api.subscan import PolkadotSubscanApi
from blockapi.v2.api.terra import TerraApi
from blockapi.v2.api.trezor import (
    TrezorBitcoin1Api,
    TrezorBitcoin2Api,
    TrezorLitecoinApi,
)

# tasks:
# - replace IBalance with BalanceMixin
# - create test method for fetch
# - create test method for parse
# - remove get_balances
# - implement fetch
# - implement parse
# - update __init__.py here
# - update import in tests

# terra
# perpetual
# synthetix
# covalenth
# debank
#   add fetched protocols to balance response
#   parse fetched protocols there

# cosmos
