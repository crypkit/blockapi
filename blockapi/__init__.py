import random
from .services import BlockchainAPI
import blockapi.api
import inspect

def get_random_api_class_for_coin(currency_id, exclude=[]):
    api_classes = get_api_classes_for_coin(currency_id)
    api_classes = [cl for cl in api_classes if not (cl in exclude)]
    return random.choice(api_classes) if api_classes else None

def get_api_classes_for_coin(currency_id):
    return [i for i in get_active_api_classes() if
            i.currency_id and
            i.currency_id == currency_id]

def get_all_supported_coins():
    return list(set(c.currency_id for c in get_active_api_classes()
           if c.currency_id))

def get_active_api_classes():
    #inheritors = _inheritors(BlockchainAPI)
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
    return [getattr(class_name,x) for x in dir(class_name) if not x.startswith('__')]

def _get_all_inheritors():
    all_inheritors = []

    tridy = _get_subclasses(blockapi.api)

    for trida in tridy:
        tridy_sub = _get_subclasses(trida)
        for trida_sub in tridy_sub:
            if inspect.isclass(trida_sub):
                if blockapi.services.BlockchainAPI in trida_sub.__bases__:
                    all_inheritors.append(trida_sub)
                    grandchildren = _inheritors(trida_sub)
                    if len(grandchildren) > 0:
                        all_inheritors += _inheritors(trida_sub)

    return all_inheritors

