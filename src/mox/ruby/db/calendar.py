import numpy as np

from ._base import _Land
from ._enclosed import CALENDARPATH, Path
from .misc import find_land_from, lazy_date


class Calendar(_Land):
    def __init__(self, land_path) -> None:
        path = Path.aspath(land_path)
        if not path.exists():
            path = find_land_from(path, CALENDARPATH)
            if path is None:
                raise ValueError(f"Can not find Calendar with name or path<{land_path}>")
        super().__init__(path)

    def get_next_date(self):
        pass

    def get_last_date(self):
        pass

    def get_dates_btw(self, st, ed=None):
        dates = np.load(self._path.join("dates.npy"))
        st = np.searchsorted(dates, lazy_date(st))
        ed = None if ed is None else np.searchsorted(dates, lazy_date(ed))
        return dates[st:ed]

    def get_cache(self, key):
        path = self._path.extend("cache", f"{key}.npy")
        return np.load(path)
