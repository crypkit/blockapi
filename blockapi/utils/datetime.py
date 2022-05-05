from datetime import datetime
from typing import Union

from dateutil.parser import parse as parse_date


def parse_dt(dt: Union[str, int, float]) -> datetime:
    """
    Convert datetime from string or timestamp into `datetime.datetime`
    """
    if isinstance(dt, str):
        return parse_date(dt)
    elif isinstance(dt, int):
        return datetime.fromtimestamp(dt)
    elif isinstance(dt, float):
        return datetime.fromtimestamp(dt)
    else:
        raise TypeError(f'Type {type(dt)} is not supported.')
