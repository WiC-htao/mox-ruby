__version__ = "0.0.1"

from .constants import RUNNING_TYPE, DATABASE

if RUNNING_TYPE == "RSRH":
    from ._rsrh_defaults import BIZDAYS

    BIZDAYS = DATABASE.get_bizdays(BIZDAYS)
