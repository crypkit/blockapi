from datetime import datetime
from decimal import Decimal


def test_can_parse_usage(usage_parser, debank_usage_response):
    parsed = usage_parser.parse(debank_usage_response)
    assert parsed.balance == Decimal('351014')
    assert len(parsed.stats) == 31

    stats = parsed.stats[0]
    assert stats.remains == Decimal('351978')
    assert stats.usage == Decimal('13162')
    assert stats.date == datetime(2023, 3, 20)
