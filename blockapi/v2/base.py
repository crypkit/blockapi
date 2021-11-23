from abc import ABC
from typing import Dict, Optional
from urllib.parse import urljoin

import attr
import httpx

from .models import Blockchain, Coin


@attr.s(auto_attribs=True, slots=True)
class ApiOptions:
    blockchain: Blockchain
    base_url: str
    rate_limit: float = 0.0
    testnet: bool = False

    start_offset: Optional[int] = None
    max_items_per_page: Optional[int] = None
    page_offset_step: Optional[int] = None


class BlockchainApi(ABC):
    """
    General class for handling blockchain API services.
    """
    coin: Coin = NotImplemented
    api_options: ApiOptions = NotImplemented

    # {request_method: request_url}
    supported_requests: Dict[str, str] = {}

    def __init__(
        self,
        address: str,
        api_key: Optional[str] = None,
        client: Optional[httpx.Client] = None
    ):
        self.address = address
        self.api_key = api_key
        self._client = client if client is not None else self._default_client()

    def request(
        self,
        request_method: str,
        body: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **req_args
    ) -> Dict:
        """
        Call specific request method with params and return raw response.
        """
        url = self._build_request_url(request_method, **req_args)

        if body is None:
            body = {}
        if headers is None:
            headers = {}

        # if body is passed, use post
        if body is not None:
            response = self._client.post(url, data=body, headers=headers)
        else:
            response = self._client.get(url, headers=headers)

        if response.status_code != 200:
            self._raise_from_response(response)

        return response.json()

    def _build_request_url(self, request_method: str, **req_args):
        path_url = self.supported_requests.get(request_method)
        if path_url is not None:
            path_url = path_url.format(**req_args)

        return urljoin(self.api_options.base_url, path_url)

    @staticmethod
    def _default_client() -> httpx.Client:
        return httpx.Client(timeout=20.0)

    @staticmethod
    def _raise_from_response(response: httpx.Response) -> None:
        response.raise_for_status()

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(coin={self.coin.name},address={self.address})"
        )


class InvalidAddressException(Exception):
    pass
