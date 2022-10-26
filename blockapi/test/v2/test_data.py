import os

import pytest

from blockapi.v2.api.cosmos import CosmosApi, CosmosApiBase
from blockapi.v2.api.covalenth.arbitrum import ArbitrumCovalentApi
from blockapi.v2.api.covalenth.astar import AstarCovalentApi
from blockapi.v2.api.covalenth.avalanche import AvalancheCovalentApi
from blockapi.v2.api.covalenth.axie import AxieCovalentApi
from blockapi.v2.api.covalenth.base import CovalentApiBase
from blockapi.v2.api.covalenth.binance_smart_chain import BscCovalentApi
from blockapi.v2.api.covalenth.fantom import FantomCovalentApi
from blockapi.v2.api.covalenth.heco import HECOCovalentApi
from blockapi.v2.api.covalenth.iotex import IoTEXCovalentApi
from blockapi.v2.api.covalenth.klaytn import KlaytnCovalentApi
from blockapi.v2.api.covalenth.moonbeam import MoonBeamCovalentApi
from blockapi.v2.api.covalenth.palm import PalmCovalentApi
from blockapi.v2.api.covalenth.polygon import PolygonCovalentApi
from blockapi.v2.api.covalenth.rsk import RskCovalentApi
from blockapi.v2.api.debank import DebankApi
from blockapi.v2.api.ethplorer import EthplorerApi
from blockapi.v2.api.optimistic_etherscan import OptimismEtherscanApi
from blockapi.v2.api.perpetual import PerpetualApi
from blockapi.v2.api.solana import SolanaApi
from blockapi.v2.api.subscan import PolkadotSubscanApi
from blockapi.v2.api.synthetix import SynthetixApi
from blockapi.v2.api.terra import TerraApi

# TODO create method for auto loading all classes
from blockapi.v2.base import IBalance
from blockapi.v2.coins import (
    COIN_ATOM,
    COIN_AVAX,
    COIN_BNB,
    COIN_DOT,
    COIN_ETH,
    COIN_FTM,
    COIN_HT,
    COIN_IOTX,
    COIN_KLAY,
    COIN_MATIC,
    COIN_MOVR,
    COIN_PALM,
    COIN_RON,
    COIN_RSK,
    COIN_SDN,
    COIN_SOL,
    COIN_TERRA,
)

COVALENT_API_KEY = os.getenv("COVALENT_API_KEY")
DEBANK_API_KEY = os.getenv("DEBANK_API_KEY")

API_CLASSES = [
    EthplorerApi,
    SolanaApi,
    TerraApi,
    ArbitrumCovalentApi,
    AstarCovalentApi,
    AvalancheCovalentApi,
    AxieCovalentApi,
    BscCovalentApi,
    EthplorerApi,
    FantomCovalentApi,
    HECOCovalentApi,
    IoTEXCovalentApi,
    KlaytnCovalentApi,
    MoonBeamCovalentApi,
    PalmCovalentApi,
    PolygonCovalentApi,
    RskCovalentApi,
    OptimismEtherscanApi,
    DebankApi,
    PolkadotSubscanApi,
    CosmosApi,
    SynthetixApi,
    PerpetualApi,
]

NON_EMPTY_VALID_ADDRESSES_BY_SYMBOL = {
    COIN_ETH.symbol: [
        '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
    ],
    COIN_SOL.symbol: [
        '31dpiondDhZaqK23Re8kzkhY6CFEG9ZTQnr3shQm7g8b',
    ],
    COIN_TERRA.symbol: [
        'terra1yltenl48mhl370ldpyt83werd9x3s645509gaf',
    ],
    COIN_SDN.symbol: [
        '0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de',
    ],
    COIN_AVAX.symbol: [
        '0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de',
    ],
    COIN_RON.symbol: [
        '0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de',
    ],
    COIN_BNB.symbol: [
        '0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de',
    ],
    COIN_FTM.symbol: [
        '0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de',
    ],
    COIN_HT.symbol: [
        '0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de',
    ],
    COIN_IOTX.symbol: [
        '0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de',
    ],
    COIN_KLAY.symbol: [
        '0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de',
    ],
    COIN_MOVR.symbol: [
        '0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de',
    ],
    COIN_PALM.symbol: [
        '0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de',
    ],
    COIN_MATIC.symbol: [
        '0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de',
    ],
    COIN_RSK.symbol: [
        '0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de',
    ],
    COIN_DOT.symbol: ['15j4dg5GzsL1bw2U2AWgeyAk6QTxq43V7ZPbXdAmbVLjvDCK'],
    COIN_ATOM.symbol: ['cosmos1r4v9t46zyu6df0jwtmtpn0pq864dpn7c5sha5u'],
}

BAD_ADDRESSES = [
    '1',
    '10000',
    'AAAAA',
    '0x123',
    'ýžýščš&^^~',
    '0xAF3E9eF83B1dc9Db18cD5923e3112F6Cd8bfDAeX',
    '0xAF3E9eF83B1dc9Db18cD5923e3112F6Cd8bfDAeDD',
]


def yield_api_instances():
    for api_cls in yield_covalent_api_classes():
        yield _pytest_param(api_cls(api_key=COVALENT_API_KEY))

    for api_cls in yield_api_ibalance_classes():
        yield _pytest_param(api_cls())


def _pytest_param(api_inst):
    return pytest.param(api_inst, id=str(api_inst))


def yield_covalent_api_classes():
    return CovalentApiBase.__subclasses__()


def yield_api_ibalance_classes():
    return [
        x
        for x in IBalance.__subclasses__()
        if not issubclass(x, (CosmosApiBase, CovalentApiBase, DebankApi))
    ]


def yield_all_api_classes():
    return [x for x in IBalance.__subclasses__()]


def yield_debank_address():
    result = []
    for key, items in NON_EMPTY_VALID_ADDRESSES_BY_SYMBOL.items():
        if key in (
            COIN_TERRA.symbol,
            COIN_SOL.symbol,
            COIN_DOT.symbol,
            COIN_ATOM.symbol,
        ):
            continue

        for item in items:
            result.append(pytest.param(item, id=key))

    return result
