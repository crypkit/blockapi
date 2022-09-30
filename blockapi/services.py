import inspect
from abc import ABC, abstractmethod
from datetime import datetime
from time import sleep

import cfscrape
import requests

import blockapi

cfscrape.DEFAULT_CIPHERS += ':!SHA'


class Service(ABC):
    """General class for handling blockchain API services."""

    active = True

    base_url = None
    rate_limit = 0

    # {request_method: request_url}
    supported_requests = {}

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.last_response = None
        self.last_response_time = None

    def build_request_url(self, request_method, **params):
        path_url = self.supported_requests.get(request_method)
        if path_url:
            return self.base_url + path_url.format(**params)
        return self.base_url

    def request(
        self,
        request_method,
        with_rate_limit=False,
        with_cloudflare=False,
        body=None,
        headers=None,
        **params
    ):
        request_url = self.build_request_url(request_method, **params)

        if not request_url:
            return None

        if not body:
            body = {}

        if not headers:
            headers = {}

        if with_cloudflare:
            reqobj = cfscrape.create_scraper()
        else:
            reqobj = requests

        if with_rate_limit and self.rate_limit:
            self.wait_for_next_request()

        # if body is passed, use post
        if body:
            response = reqobj.post(request_url, data=body, headers=headers)
        else:
            response = reqobj.get(request_url, headers=headers)

        self.last_response = response
        self.last_response_time = datetime.now()

        if response.status_code != 200:
            self.process_error_response(response)

        return response.json()

    def wait_for_next_request(self):
        if not self.last_response_time:
            return

        diff = (datetime.now() - self.last_response_time).total_seconds()
        wait = self.rate_limit - diff

        if wait > 0:
            sleep(wait)

        # use date from last response
        # doesn't work very good, time on server can differ from local time
        # if self.last_response.headers.get('Date'):
        # last_resp_time = date_parse(self.last_response.headers.get('Date'))
        # last_resp_time.replace(tzinfo=UTC)
        # wait_until = last_resp_time + timedelta(seconds=self.rate_limit)
        #
        # now = datetime.utcnow().replace(tzinfo=UTC)

    def process_error_response(self, response):
        if response.status_code == 500:
            raise InternalServerError('Error 500: Internal Server Error.')
        if response.status_code == 502:
            raise BadGateway('Error 502: Bad Gateway.')
        if response.status_code == 504:
            raise GatewayTimeOut('Error 504: Gateway timeout.')

        raise APIError(
            'Following error occured: {}, status code: {}.'.format(
                response.text, response.status_code
            )
        )


# Decorator that set default args
def set_default_args_values(f):
    def wrapper(*args, **kwargs):
        args, kwargs = _set_default_arg(
            f, 'offset', args[0].start_offset, *args, **kwargs
        )
        args, kwargs = _set_default_arg(
            f, 'limit', args[0].max_items_per_page, *args, **kwargs
        )

        return f(*args, **kwargs)

    def _set_default_arg(f_, arg_name, default_value, *args, **kwargs):
        sig = inspect.signature(f_)
        arg_idx, _ = next(
            (i, par)
            for i, (name, par) in enumerate(sig.parameters.items())
            if name == arg_name
        )

        # check if its argument is in *args
        if len(args) > arg_idx:
            if args[arg_idx] is None:
                list_args = list(args)
                list_args[arg_idx] = default_value
                args = tuple(list_args)

        elif kwargs.get(arg_name) is None:
            kwargs[arg_name] = default_value

        return args, kwargs

    return wrapper


def on_failure_return_none():
    def decorate(f):
        def applicator(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except (APIError, InternalServerError, BadGateway, GatewayTimeOut):
                return None

        return applicator

    return decorate


# Exceptions
class APIError(Exception):
    pass


class AddressNotExist(APIError):
    pass


class APIKeyMissing(APIError):
    pass


# 500
class InternalServerError(APIError):
    pass


# 502
class BadGateway(APIError):
    pass


# 504
class GatewayTimeOut(APIError):
    pass


class BlockchainInterface(ABC):
    coef = 1
    start_offset = 0
    max_items_per_page = None
    page_offset_step = 1
    confirmed_num = 0
    testnet_url = None
    xpub_support = False

    def __init__(self, address):
        self.address = address

    @abstractmethod
    def get_balance(self):
        raise NotImplementedError()

    @set_default_args_values
    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        """Loads txs for single address."""
        return []

    @staticmethod
    def filter_unconfirmed_txs(txs):
        return [t for t in txs if t.get('confirmed') in [True, None]]


class BlockchainAPI(Service, BlockchainInterface, ABC):
    symbol = None

    def __init__(self, address, api_key=None):
        Service.__init__(self, api_key)
        BlockchainInterface.__init__(self, address)

        self.address_info = blockapi.get_address_info(self.symbol.lower(), address)
        self.update_network()

    def update_network(self):
        if self.address_info.network == 'test':
            if self.testnet_url:
                self.base_url = self.testnet_url
            else:
                raise ValueError("API doesn't support testnet.")

    def _load(self, data):
        from decimal import Decimal

        if isinstance(data, dict):
            for key in data:
                data[key] = self._load(data[key])
            return data
        elif isinstance(data, list):
            for i, elem in enumerate(data):
                data[i] = self._load(elem)
            return data
        elif isinstance(data, str):
            new = None
            try:
                new = Decimal(data)
            except ValueError:
                new = data
            finally:
                return new
        else:
            return data
