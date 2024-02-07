import re

from blockapi.api import SolanaApi
from blockapi.test.v2.test_data import (
    get_debank_addresses,
    yield_api_balance_classes,
    yield_covalent_api_classes,
)
from blockapi.v2.api import DebankApi, EthplorerApi, PerpetualApi
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
from blockapi.v2.api.synthetix import SynthetixApi


def test_enumerate_subclasses():
    classes = [x.__name__ for x in yield_api_balance_classes()]

    assert classes
    assert SolanaApi.__name__ in classes
    assert EthplorerApi.__name__ in classes
    assert DebankApi.__name__ not in classes
    assert PerpetualApi.__name__ not in classes
    assert SynthetixApi.__name__ not in classes

    for cls in classes:
        assert 'Base' not in cls


def test_enumerate_covalent_all_classes():
    assert [
        ArbitrumCovalentApi,
        AstarCovalentApi,
        AvalancheCovalentApi,
        AxieCovalentApi,
        BscCovalentApi,
        EthCovalentApi,
        FantomCovalentApi,
        HECOCovalentApi,
        IoTEXCovalentApi,
        KlaytnCovalentApi,
        MoonBeamCovalentApi,
        PalmCovalentApi,
        PolygonCovalentApi,
        RskCovalentApi,
    ] == sorted(yield_covalent_api_classes(), key=lambda x: x.__name__)


def test_yield_debank_address():
    for param in get_debank_addresses():
        for address in param.values:
            assert re.match('^0x[a-fA-F0-9]{40}$', address)
