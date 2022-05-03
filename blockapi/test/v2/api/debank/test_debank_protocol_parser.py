from decimal import Decimal

import pytest

from blockapi.v2.api.debank import DebankProtocolParser

# noinspection PyUnresolvedReferences
from fixtures import (
    protocol_parser,
    yflink_protocol_response
)


def test_can_parse_protocol_id(protocol_parser, yflink_protocol_response):
    parsed = protocol_parser.parse(yflink_protocol_response)
    assert parsed['yflink'].protocol_id == 'yflink'


def test_can_parse_protocol_chain(protocol_parser, yflink_protocol_response):
    parsed = protocol_parser.parse(yflink_protocol_response)
    assert parsed['yflink'].chain == 'eth'


def test_can_parse_protocol_name(protocol_parser, yflink_protocol_response):
    parsed = protocol_parser.parse(yflink_protocol_response)
    assert parsed['yflink'].name == 'YFLink'


def test_can_parse_protocol_name(protocol_parser, yflink_protocol_response):
    parsed = protocol_parser.parse(yflink_protocol_response)
    assert parsed['yflink'].name == 'YFLink'


def test_can_parse_protocol_site_url(protocol_parser, yflink_protocol_response):
    parsed = protocol_parser.parse(yflink_protocol_response)
    assert parsed['yflink'].site_url == 'https://linkswap.app'


def test_can_parse_protocol_logo_url(protocol_parser, yflink_protocol_response):
    parsed = protocol_parser.parse(yflink_protocol_response)
    assert parsed['yflink'].logo_url == 'https://static.debank.com/image/project/logo_url/yflink' \
                                        '/a43f4e05d96b559fecf4984f760bf737.png'


def test_can_parse_protocol_has_supported_portfolio(protocol_parser, yflink_protocol_response):
    parsed = protocol_parser.parse(yflink_protocol_response)
    assert parsed['yflink'].has_supported_portfolio is False


def test_can_parse_protocol_has_user_deposit(protocol_parser, yflink_protocol_response):
    parsed = protocol_parser.parse(yflink_protocol_response)
    assert parsed['yflink'].user_deposit == Decimal('1234.5')
