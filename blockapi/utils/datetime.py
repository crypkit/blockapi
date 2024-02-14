from datetime import datetime, timezone
from typing import Union

from dateutil.parser import parse as parse_date


def parse_dt(dt: Union[str, int, float]) -> datetime:
    """
    Convert datetime from string or timestamp into `datetime.datetime`
    """
    if isinstance(dt, str):
        try:
            return datetime.fromtimestamp(int(dt), tz=timezone.utc)
        except ValueError:
            return parse_date(dt)
    elif isinstance(dt, int) or isinstance(dt, float):
        return datetime.fromtimestamp(dt, tz=timezone.utc)
    else:
        raise TypeError(f'Type {type(dt)} is not supported.')
