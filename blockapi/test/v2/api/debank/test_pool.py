from datetime import datetime
from decimal import Decimal

from fixtures import (
   protocol_yflink,
   pool_item,
   balance_item
)


def test_pool_append_items_copies_pool_id(pool_item, balance_item):
    pool = pool_item.append_items([balance_item])
    assert pool.pool_id == '123'


def test_pool_append_items_copies_protocol(protocol_yflink, pool_item, balance_item):
    pool = pool_item.append_items([balance_item])
    assert pool.protocol == protocol_yflink


def test_pool_append_items_appends_items(pool_item, balance_item):
    pool = pool_item.append_items([balance_item])
    assert len(pool.items) == 2


def test_pool_append_items_copies_locked_until(pool_item, balance_item):
    pool = pool_item.append_items([balance_item])
    assert pool.locked_until == datetime(2022, 7, 21, 2, 0, 0)


def test_pool_append_items_copies_health_rate(pool_item, balance_item):
    pool = pool_item.append_items([balance_item])
    assert pool.health_rate == Decimal('0.99')
