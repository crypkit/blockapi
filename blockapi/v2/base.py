from abc import ABC
from typing import Dict, List, Optional, Tuple, Type, Union
from urllib.parse import urljoin

from requests import HTTPError, Response, Session

from blockapi.v2.models import (
    ApiOptions,
    BalanceItem,
    Coin,
    FetchResult,
    ParseResult,
    Pool,
    TransactionItem,
)


class CustomizableBlockchainApi(ABC):
    """
    Class for handling blockchain API services with customizable base URL,
    e.g. proxy, testnet, RPC services, alternative sources
    """

    coin: Coin = NotImplemented
    api_options: ApiOptions = NotImplemented

    # {request_method: request_url}
    supported_requests: Dict[str, str] = {}

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.api_key = api_key
        self._session = Session()
        self.base_url = base_url or self.api_options.base_url

        if not self.base_url:
            raise NotImplementedError(
                'api_options.base_url is not set and no base_url was provided'
            )

    def __del__(self):
        self._session.close()

    def get(
        self,
        request_method: str,
        headers=None,
        **req_args,
    ) -> Dict:
        """
        Call specific request method with params and return raw response.
        """
        response = self._get_response(request_method, headers, req_args)
        return self._check_and_get_from_response(response)

    def get_data(
        self, request_method: str, headers=None, **req_args
    ) -> Tuple[int, Optional[Union[dict, list]], Optional[list]]:
        response = self._get_response(request_method, headers, req_args)
        if response.status_code == 200:
            return response.status_code, response.json(), None

        return response.status_code, None, [self._get_reason(response)]

    def _get_response(self, request_method, headers, req_args):
        url = self._build_request_url(request_method, **req_args)
        response = self._session.get(url, headers=headers)
        return response

    def _build_request_url(self, request_method: str, **req_args):
        path_url = self.supported_requests.get(request_method)
        if path_url is not None:
            path_url = path_url.format(**req_args)

        return urljoin(self.base_url, path_url)

    def post(self, request_method=None, body=None, json=None, headers=None):
        """
        Call request using json.
        """
        url = (
            self._build_request_url(request_method)
            if request_method
            else self.api_options.base_url
        )
        response = self._session.post(url, data=body, json=json, headers=headers)
        return self._check_and_get_from_response(response)

    def _check_and_get_from_response(self, response: Response) -> Dict:
        if response.status_code != 200:
            self._raise_from_response(response)
        self._opt_raise_on_other_error(response)

        return response.json()

    @staticmethod
    def _get_reason(response):
        reason = response.reason
        if not reason and response.status_code >= 400:
            return f'Error {response.status_code}'

        if not isinstance(reason, bytes):
            return reason

        try:
            return reason.decode("utf-8")
        except UnicodeDecodeError:
            return reason.decode("iso-8859-1")

    @staticmethod
    def _raise_from_response(response: Response) -> None:
        try:
            response.raise_for_status()
        except HTTPError as e:
            raise ApiException(e)

    def _opt_raise_on_other_error(self, response: Response) -> None:
        # implement in child
        return

    def __repr__(self):
        if self.coin is None:
            return self.__class__.__name__

        return f'{self.__class__.__name__}(coin={self.coin.name})'


class BlockchainApi(CustomizableBlockchainApi, ABC):
    """
    General class for handling blockchain API services.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=None, api_key=api_key)


class IBalance(ABC):
    def get_balance(self, address: str) -> List[BalanceItem]:
        raise NotImplementedError


class ITransactions(ABC):
    def get_transactions(
        self,
        address: str,
        *,
        offset: int = 0,
        limit: int = 10,
        unconfirmed: bool = False,
    ) -> List[TransactionItem]:
        raise NotImplementedError


class IPortfolio(ABC):
    def get_portfolio(self, address: str) -> List[Pool]:
        raise NotImplementedError


class ApiException(Exception):
    pass


class InvalidAddressException(ApiException):
    pass


class IBlockchainFetcher(ABC):
    def fetch_balances(self, address: str) -> FetchResult:
        raise NotImplementedError


class IBlockchainParser(ABC):
    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        raise NotImplementedError


class BalanceMixin(IBalance, IBlockchainParser, IBlockchainFetcher):
    def get_balance(self, address: str) -> list[BalanceItem]:
        data = self.fetch_balances(address)
        if data.errors:
            raise ApiException(data.errors[0])

        parsed = self.parse_balances(data)
        return parsed.balances
