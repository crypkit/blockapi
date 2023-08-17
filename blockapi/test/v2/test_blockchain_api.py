from abc import ABC

import pytest

from blockapi.v2.base import CustomizableBlockchainApi
from blockapi.v2.models import ApiOptions, Blockchain, FetchResult


def test_not_implemented_base_url():
    with pytest.raises(NotImplementedError):
        _ = WrongApi()


class WrongApi(CustomizableBlockchainApi):
    api_options = ApiOptions(
        blockchain=Blockchain.ETHEREUM,
        base_url="",
    )
