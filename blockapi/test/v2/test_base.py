import pytest

from blockapi.v2.base import CustomizableBlockchainApi
from blockapi.v2.models import ApiOptions, Blockchain


def test_not_implemented_base_url():
    with pytest.raises(NotImplementedError):
        api = WrongApi()


class WrongApi(CustomizableBlockchainApi):
    api_options = ApiOptions(
        blockchain=Blockchain.ETHEREUM,
        base_url="",
    )
