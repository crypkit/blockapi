from decimal import Decimal

from blockapi.utils.num import decimals_to_raw


def test_decimals_to_raw():
    assert decimals_to_raw("1.2", 2) == Decimal(120)
