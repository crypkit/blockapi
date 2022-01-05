import os
import time
from typing import Type

import pytest

from blockapi.v2.api.covalenth.arbitrum import ArbitrumCovalentApi
from blockapi.v2.api.covalenth.astar import AstarCovalentApi
from blockapi.v2.api.covalenth.avalanche import AvalancheCovalentApi
from blockapi.v2.api.covalenth.axie import AxieCovalentApi
from blockapi.v2.api.covalenth.base import CovalentApiBase
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

covalent_api_key = os.getenv("COVALENT_API_KEY")
API_BASE_RATE_LIMIT = 0.5


@pytest.mark.parametrize(
    "api_class, address",
    [
        (ArbitrumCovalentApi, "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"),
        (AstarCovalentApi, "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"),
        (AvalancheCovalentApi, "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"),
        (AxieCovalentApi, "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"),
        (BscCovalentApi, "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"),
        (EthCovalentApi, "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"),
        (FantomCovalentApi, "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"),
        (HECOCovalentApi, "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"),
        (IoTEXCovalentApi, "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"),
        (KlaytnCovalentApi, "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"),
        (MoonBeamCovalentApi, "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"),
        (PalmCovalentApi, "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"),
        (PolygonCovalentApi, "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"),
        (RskCovalentApi, "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"),
    ],
)
def test_get_balances(api_class: Type[CovalentApiBase], address: str) -> None:
    assert covalent_api_key
    assert api_class(api_key=covalent_api_key).get_balance(address)

    time.sleep(API_BASE_RATE_LIMIT)
