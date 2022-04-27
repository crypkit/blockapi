# noinspection PyUnresolvedReferences
from fixtures import (
    protocol_cache,

    protocol_yflink,
    yflink_cache_data
)


def test_protocol_cache_has_timeout(protocol_cache):
    assert protocol_cache._timeout == 3600


def test_needs_update_returns_true_after_creating_cache(protocol_cache):
    assert protocol_cache.needs_update() is True


def test_get_with_non_existent_protocol_returns_none(protocol_cache):
    assert protocol_cache.get('xxx') is None


def test_cache_update_items(protocol_cache, yflink_cache_data, protocol_yflink):
    protocol_cache.update(yflink_cache_data)
    assert protocol_cache.get('yflink') is protocol_yflink


def test_cache_updating_items_changes_timeout(protocol_cache, yflink_cache_data):
    protocol_cache.update(yflink_cache_data)
    assert protocol_cache.needs_update() is False
