from datetime import datetime
from decimal import Decimal


def test_pool_append_items_copies_data(protocol_yflink, pool_item, balance_item):
    pool = pool_item.append_items([balance_item])
    assert pool.pool_id == '123'
    assert pool.protocol == protocol_yflink
    assert pool.locked_until == datetime(2022, 7, 21, 2, 0, 0)
    assert pool.health_rate == Decimal('0.99')


def test_pool_append_items_appends_items(pool_item, balance_item):
    pool = pool_item.append_items([balance_item])
    assert len(pool.items) == 2
