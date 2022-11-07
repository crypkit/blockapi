from blockapi.test.v2.test_data import (
    yield_api_ibalance_classes,
    yield_covalent_api_classes,
    yield_debank_address,
)
from blockapi.v2.api.covalenth.arbitrum import ArbitrumCovalentApi
from blockapi.v2.api.covalenth.astar import AstarCovalentApi
from blockapi.v2.api.covalenth.avalanche import AvalancheCovalentApi
from blockapi.v2.api.covalenth.axie import AxieCovalentApi
from blockapi.v2.api.covalenth.binance_smart_chain import BscCovalentApi
from blockapi.v2.api.covalenth.ethereum import EthCovalentApi
from blockapi.v2.api.covalenth.fantom import FantomCovalentApi
from blockapi.v2.api.covalenth.heco import HECOCovalentApi
from blockapi.v2.api.covalenth.iotex import IoTEXCovalentApi
from blockapi.v2.api.covalenth.klaytn import KlaytnCovalentApi
from blockapi.v2.api.covalenth.moonbeam import MoonBeamCovalentApi
from blockapi.v2.api.covalenth.palm import PalmCovalentApi
from blockapi.v2.api.covalenth.polygon import PolygonCovalentApi
from blockapi.v2.api.covalenth.rsk import RskCovalentApi


def test_enumerate_subclasses():
    assert len(yield_api_ibalance_classes()) == 5


def test_enumerate_covalent_all_classes():
    assert [
        ArbitrumCovalentApi,
        AstarCovalentApi,
        AvalancheCovalentApi,
        AxieCovalentApi,
        BscCovalentApi,
        FantomCovalentApi,
        HECOCovalentApi,
        IoTEXCovalentApi,
        KlaytnCovalentApi,
        MoonBeamCovalentApi,
        PalmCovalentApi,
        PolygonCovalentApi,
        RskCovalentApi,
        EthCovalentApi,
    ] == yield_covalent_api_classes()


def test_enumerate_covalent_classes():
    assert len(yield_covalent_api_classes()) == 14


def test_yield_debank_address():
    assert len(yield_debank_address()) == 13
