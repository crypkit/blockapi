from decimal import Decimal


def safe_decimal(number) -> Decimal:
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
