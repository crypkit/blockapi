import inspect
from abc import ABC, abstractmethod
from time import sleep

import cfscrape
import requests

import blockapi


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

    def build_request_url(self, request_method, **params):
        path_url = self.supported_requests.get(request_method)
        if path_url:
            return self.base_url + path_url.format(**params)
        return None

    def request(self, request_method, with_rate_limit=True, with_cloudflare=False,
                body=None, headers=None, **params):
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

        if with_rate_limit:
            self.wait_for_next_request()

        try:
            # if body is passed, use post
            if body:
                response = reqobj.post(request_url, data=body, headers=headers)
            else:
                response = reqobj.get(request_url)
            self.last_response = response
        except Exception as e:
            raise e

        if response.status_code != 200:
            self.process_error_response(response)

        return response.json()

    def wait_for_next_request(self):
        # TODO - store timestamp of last request and wait till rate limit
        # is >= then current timestamp and timestamp of last request
        sleep(self.rate_limit)

    def process_error_response(self, response):
        if response.status_code == 500:
            raise InternalServerError('Error 500: Internal Server Error.')
        if response.status_code == 502:
            raise BadGateway('Error 502: Bad Gateway.')
        if response.status_code == 504:
            raise GatewayTimeOut('Error 504: Gateway timeout.')

        raise APIError('Following error occured: {}, status code: {}.'.format(
            response.text, response.status_code))


# Decorator that set default args
def set_default_args_values(f):
    def wrapper(*args, **kwargs):
        args, kwargs = _set_default_arg(
            f, 'offset', args[0].start_offset, *args, **kwargs)
        args, kwargs = _set_default_arg(
            f, 'limit', args[0].max_items_per_page, *args, **kwargs)

        return f(*args, **kwargs)

    def _set_default_arg(f, arg_name, default_value, *args, **kwargs):
        sig = inspect.signature(f)
        arg_idx, _ = next((i, par) for i, (name, par)
                          in enumerate(sig.parameters.items()) if name == arg_name)

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


# Exceptions
class APIError(Exception):
    pass


class AddressNotExist(APIError):
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

    def __init__(self, address):
        self.address = address

    @abstractmethod
    def get_balance(self):
        raise NotImplementedError()

    @set_default_args_values
    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        """Loads txs for single address."""
        return []

    def parse_tx(self, tx):
        """Parse txs into general structure."""
        return tx

    @staticmethod
    def filter_unconfirmed_txs(txs):
        return [t for t in txs if t.get('confirmed') in [True, None]]


def check_obligatory_fields(method, args, kwargs, obligatory_fields):
    response = method(*args, **kwargs)
    if not response:
        return True

    response_keys = []
    if type(response) == dict:
        response_keys = response.keys
    elif type(response) == list:
        response_keys = response[0].keys

    missing_fields = []
    for obl_field in obligatory_fields:
        if obl_field not in response_keys:
            missing_fields.append(obl_field)


class BlockchainAPI(Service, BlockchainInterface, ABC):
    currency_id = None

    def __init__(self, address, api_key=None):
        if not blockapi.check_address_valid(self.currency_id, address):
            raise ValueError('Not a valid {} address: {}'.format(self.currency_id, address))

        Service.__init__(self, api_key)
        BlockchainInterface.__init__(self, address)
