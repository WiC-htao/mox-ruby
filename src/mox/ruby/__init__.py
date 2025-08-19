__version__ = "0.0.1"

from .constants import DATABASE, RUNNING_TYPE
from .date import get_date

__all__ = ["RUNNING_TYPE", "get_date", "BIZDAYS"]
if RUNNING_TYPE == "RSRH":
    from ._rsrh_defaults import BIZDAYS as _BIZDAYS

    BIZDAYS = DATABASE.get_bizdays(_BIZDAYS)
