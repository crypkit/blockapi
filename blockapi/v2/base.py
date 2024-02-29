import json
import logging
import time
from abc import ABC
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from urllib.parse import urljoin

from requests import HTTPError, Response, Session
from requests.structures import CaseInsensitiveDict

from blockapi.utils.datetime import parse_dt
from blockapi.v2.models import (
    ApiOptions,
    BalanceItem,
    Coin,
    FetchResult,
    ParseResult,
    Pool,
    TransactionItem,
)

logger = logging.getLogger(__name__)


class ISleepProvider(ABC):
    def sleep(self, url: str, seconds: float) -> None:
        raise NotImplementedError


class SleepProvider(ISleepProvider):
    def sleep(self, url: str, seconds: float):
        time.sleep(seconds)


class CustomizableBlockchainApi(ABC):
    """
    Class for handling blockchain API services with customizable base URL,
    e.g. proxy, testnet, RPC services, alternative sources
    """

    base_url: str

    coin: Coin = NotImplemented
    api_options: ApiOptions = NotImplemented

    # {request_method: request_url}
    supported_requests: Dict[str, str] = {}

    json_parse_args = dict()
    max_rate_limit_retries = 5

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        sleep_provider: Optional[ISleepProvider] = None,
    ):
        self.api_key = api_key
        self._session = Session()
        self.base_url = base_url or self.api_options.base_url
        self.sleep_provider = sleep_provider

        if not self.base_url:
            raise NotImplementedError(
                'api_options.base_url is not set and no base_url was provided'
            )

    def __del__(self):
        self._session.close()

    def get(
        self,
        request_method: str,
        headers: Optional[dict[str, any]] = None,
        params: Optional[dict[str, any]] = None,
        **req_args,
    ) -> Dict:
        """
        Call specific request method with params and return raw response.
        """
        response = self._get_response(request_method, headers, params, req_args)
        return self._check_and_get_from_response(response)

    def get_data(
        self,
        request_method: str,
        headers: Optional[dict[str, any]] = None,
        params: Optional[dict[str, any]] = None,
        extra: Optional[dict] = None,
        **req_args,
    ) -> FetchResult:
        try:
            retries = self.max_rate_limit_retries
            while True:
                response = self._get_response(request_method, headers, params, req_args)
                time = self._get_response_time(response.headers)
                if response.status_code == 200:
                    return FetchResult(
                        status_code=response.status_code,
                        headers=self._get_headers_dict(response.headers),
                        data=response.json(**self.json_parse_args),
                        extra=extra,
                        time=time,
                    )

                if response.status_code == 429 and self.sleep_provider and retries > 0:
                    retries -= 1
                    delay = response.headers.get('retry-after', '60')
                    try:
                        seconds = int(delay)
                    except ValueError:
                        seconds = 60

                    logger.warning(
                        f'Too Many Requests: Will retry after {seconds}s sleep. Remaining attempts {retries}.'
                    )
                    self.sleep_provider.sleep(self.base_url, seconds=seconds)
                    continue

                break
            return FetchResult(
                status_code=response.status_code,
                headers=self._get_headers_dict(response.headers),
                errors=[self._get_reason(response)],
                extra=extra,
                time=time,
            )
        except Exception as ex:
            return FetchResult(
                status_code=0,
                headers=dict(),
                errors=[f'{type(ex).__name__}: {str(ex)}'],
                extra=extra,
                time=datetime.utcnow(),
            )

    def _get_response(self, request_method, headers, params, req_args):
        url = self._build_request_url(request_method, **req_args)
        response = self._session.get(url, headers=headers, params=params)
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
        url = self._build_request_url(request_method)
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
            logger.error(response.text)
            raise ApiException(e)

    def _opt_raise_on_other_error(self, response: Response) -> None:
        # implement in child
        return

    def __repr__(self):
        if self.coin is None:
            return self.__class__.__name__

        return f'{self.__class__.__name__}(coin={self.coin.name})'

    @staticmethod
    def _get_response_time(headers) -> Optional[datetime]:
        if date_str := headers.get('date'):
            return parse_dt(date_str)

        if age_str := headers.get('age'):
            return datetime.utcnow() - timedelta(seconds=int(age_str))

        return None

    @staticmethod
    def _get_headers_dict(headers: CaseInsensitiveDict[str]):
        return {k: v for k, v in headers.items()}


class BlockchainApi(CustomizableBlockchainApi, ABC):
    """
    General class for handling blockchain API services.
    """

    def __init__(
        self, api_key: Optional[str] = None, sleep_provider: ISleepProvider = None
    ):
        super().__init__(base_url=None, api_key=api_key, sleep_provider=sleep_provider)


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


class INftProvider(ABC):
    def fetch_nfts(self, address: str) -> FetchResult:
        raise NotImplementedError

    def fetch_collection_stats(self, collection: str) -> FetchResult:
        raise NotImplementedError

    def fetch_offers(self, collection: str) -> FetchResult:
        raise NotImplementedError

    def fetch_listings(self, collection: str) -> FetchResult:
        raise NotImplementedError


class INftParser(ABC):
    def parse_nfts(self, data: FetchResult) -> ParseResult:
        raise NotImplementedError

    def parse_collections(self, data: FetchResult) -> ParseResult:
        raise NotImplementedError

    def parse_offers(self, data: FetchResult) -> ParseResult:
        raise NotImplementedError

    def parse_listings(self, data: FetchResult) -> ParseResult:
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
        return parsed.data or []
