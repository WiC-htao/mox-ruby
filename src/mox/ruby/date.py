from typing import overload

from pendulum.date import Date


@overload
def get_date(year: int, month: int, day: int): ...


@overload
def get_date(yyyymmdd_int: int): ...


def get_date(*args, **kwargs) -> Date:
    if len(args) == 1 and len(kwargs) == 0:
        year, date = divmod(args[0], 10_000)
        month, day = divmod(date, 100)
        return Date(year, month, day)
    return Date(*args, **kwargs)
