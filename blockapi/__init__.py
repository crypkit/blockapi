import inspect
import random

import coinaddrng

import blockapi.api
import blockapi.utils

from .services import APIError
from .test_data import test_addresses

# currencies' ids (from coingecko.com) and symbols
COINS = {
    'binance-coin': 'BNB',
    'bitcoin': 'BTC',
    'bitcoin-cash': 'BCH',
    'bitcoin-sv': 'BSV',
    'boscoin': 'BOS',
    'cardano': 'ADA',
    'cosmos': 'ATOM',
    'decred': 'DCR',
    'dashcoin': 'DASH',
    'dogecoin': 'DOGE',
    'eos': 'EOS',
    'ethereum': 'ETH',
    'ethereum-classic': 'ETC',
    'groestlcoin': 'GRS',
    'horizen': 'ZEN',
    'litecoin': 'LTC',
    'neocoin': 'NEO',
    'ontology': 'ONT',
    'ravencoin': 'RVN',
    'stellar': 'XLM',
    'tezos': 'XTZ',
    'tron': 'TRX',
    'vechain': 'VET',
    'zcash': 'ZEC',
}


def get_balance_from_random_api(symbol, address):
    """Get balance for currency from random API
    (APIs with API keys are not supported).
    """
    return _call_method_from_random_api(symbol, address, 'get_balance')


def get_shuffled_suitable_api_classes_for_coin(symbol, address):
    api_classes = get_shuffled_api_classes_for_coin(symbol)
    filtered_api_classes = filter_suitable_api_classes(api_classes, symbol, address)
    return filtered_api_classes


def _call_method_from_random_api(symbol, address, method):
    filtered_api_classes = get_shuffled_suitable_api_classes_for_coin(symbol, address)
    for cl in filtered_api_classes:
        try:
            inst = cl(address)
            return getattr(inst, method)()
        except (APIError, Exception):
            continue
    return None


def get_shuffled_api_classes_for_coin(symbol):
    api_classes = get_api_classes_for_coin(symbol)
    random.shuffle(api_classes)
    return api_classes


def get_api_classes_for_coin(symbol):
    return [i for i in get_active_api_classes() if i.symbol and i.symbol == symbol]


def filter_suitable_api_classes(api_classes, symbol, address):
    address_info = get_address_info(symbol, address)

    filtered = api_classes
    if address_info.network == 'test':
        filtered = [c for c in filtered if c.testnet_url]
    if address_info.is_extended:
        filtered = [c for c in filtered if c.xpub_support]
    return filtered


def get_random_api_class_for_coin(symbol, exclude=None):
    api_classes = get_api_classes_for_coin(symbol)
    exclude = [] if not exclude else exclude
    api_classes = [cl for cl in api_classes if not (cl in exclude)]
    return random.choice(api_classes) if api_classes else None


def get_all_supported_coins():
    return list(set(c.symbol for c in get_active_api_classes() if c.symbol))


def get_active_api_classes():
    inheritors = _get_all_inheritors()
    return [i for i in inheritors if i.active]


def _inheritors(klass):
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses


def _get_subclasses(class_name):
    return [getattr(class_name, x) for x in dir(class_name) if not x.startswith('__')]


def _get_all_inheritors():
    all_inheritors = []

    tridy = _get_subclasses(blockapi.api)

    for trida in tridy:
        tridy_sub = _get_subclasses(trida)
        for trida_sub in tridy_sub:
            if (
                inspect.isclass(trida_sub)
                and blockapi.services.BlockchainAPI in trida_sub.__bases__
            ):
                all_inheritors.append(trida_sub)
                grandchildren = _inheritors(trida_sub)
                if len(grandchildren) > 0:
                    all_inheritors += _inheritors(trida_sub)

    return all_inheritors


def get_working_apis_for_coin(symbol, debug=False):
    coin_classes = get_api_classes_for_coin(symbol)

    if symbol in test_addresses:
        if len(test_addresses[symbol]) == 0:
            return ()
    else:
        return ()

    coin_address = test_addresses[symbol][0]
    working_apis = []

    api_ok = True
    for api_class in coin_classes:
        api_inst = api_class(coin_address)
        exception_class = None
        exception_msg = None
        try:
            api_inst.get_balance()

        except Exception as e:
            exception_class = e.__class__.__name__
            exception_msg = str(e)
            api_ok = False

        if debug:
            working_apis.append((api_class, exception_class, exception_msg))
        else:
            if api_ok:
                working_apis.append(api_class)

    return tuple(working_apis)


def get_working_apis(debug=False):
    all_coins = get_all_supported_coins()
    ok_apis = {}

    for a_coin in all_coins:
        ok_apis[a_coin] = get_working_apis_for_coin(a_coin, debug=debug)

    return ok_apis


def check_address_valid(symbol, address):
    return get_address_info(symbol, address).valid


def get_address_info(symbol: str, address: str):
    try:
        return coinaddrng.validate(symbol.lower(), address)
    except TypeError:
        # if validator for symbol doesn't exist return default object;
        # 'valid' attribute is set to True, because there may not exist
        #  validator for every supported coin
        return coinaddrng.validation.ValidationResult(
            name='',
            ticker=symbol,
            address=address.encode(),
            valid=True,
            network='',
            address_type='',
            is_extended=False,
        )
