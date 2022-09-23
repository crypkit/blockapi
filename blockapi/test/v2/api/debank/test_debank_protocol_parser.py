from decimal import Decimal

from blockapi.v2.models import Blockchain


def test_can_parse_protocol(protocol_parser, yflink_protocol_response):
    parsed = protocol_parser.parse(yflink_protocol_response)
    assert parsed['yflink'].protocol_id == 'yflink'
    assert parsed['yflink'].chain == Blockchain.ETHEREUM
    assert parsed['yflink'].name == 'YFLink'
    assert parsed['yflink'].site_url == 'https://linkswap.app'
    assert (
        parsed['yflink'].logo_url
        == 'https://static.debank.com/image/project/logo_url/yflink'
        '/a43f4e05d96b559fecf4984f760bf737.png'
    )
    assert parsed['yflink'].has_supported_portfolio is False
    assert parsed['yflink'].user_deposit == Decimal('1234.5')
