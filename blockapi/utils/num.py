from decimal import Decimal, InvalidOperation
from numbers import Number
from typing import Optional, Union

SupportsNumber = Union[str, Number]


def to_int(number: Union[int, str]):
    return int(number)


def to_decimal(number: Union[int, float, str, Decimal]) -> Decimal:
    """
    Try to convert any number to Decimal.
    Suited mostly for floats:
    >>> Decimal(1.01)
    Decimal('1.0100000000000000088817841970012523233890533447265625')
    >>> Decimal('1.01')
    Decimal('1.01')
    """
    if isinstance(number, Decimal):
        return number
    elif isinstance(number, float):
        return Decimal(str(number))
    elif isinstance(number, (int, str)):
        return Decimal(number)
    else:
        raise TypeError(f'Type {type(number)} is not supported.')


def raw_to_decimals(raw: Union[int, str], decimals: Union[int, str]) -> Decimal:
    """
    Conversion of raw (gwei/satoshi/...) format to decimals.
    """
    raw_ = to_decimal(raw)
    decimals_ = to_decimal(decimals)
    res = raw_ * pow(10, -decimals_)
    return remove_exponent(res)


def decimals_to_raw(amount: Union[int, str], decimals: Union[int, str]) -> Decimal:
    """
    Convert decimal value to raw format
    """
    amount_ = to_decimal(amount)
    decimals_ = to_decimal(decimals)
    res = amount_ * pow(10, decimals_)
    return remove_exponent(res)


def remove_exponent(d: Decimal) -> Decimal:
    """
    https://docs.python.org/3/library/decimal.html#decimal-faq
    Remove the exponent and trailing zeroes, losing significance,
    but keeping the value unchanged.
    """
    try:
        return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()
    except InvalidOperation:
        return d


def safe_opt_decimal(obj: Optional[SupportsNumber]) -> Decimal:
    """
    This function is primarily for parsing 3rd party APIs that sometimes,
    despite stating in their docs that *number* is returned, may return null.

    >>> safe_opt_decimal(None)
    Decimal('0')
    """
    if obj is None:
        return Decimal('0')
    else:
        return to_decimal(obj)


def safe_decimal(number: SupportsNumber) -> Decimal:
    """
    Try to convert any number to Decimal.
    Suited mostly for floats:
    >>> Decimal(1.01)
    Decimal('1.0100000000000000088817841970012523233890533447265625')
    >>> Decimal('1.01')
    Decimal('1.01')
    """
    if isinstance(number, Decimal):
        return number
    if isinstance(number, float):
        return Decimal(str(number))
    elif isinstance(number, (int, str)):
        return Decimal(number)
    else:
        raise TypeError(f'Type {type(number)} is not supported.')
