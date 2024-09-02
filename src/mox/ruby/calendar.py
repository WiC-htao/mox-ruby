import numpy as np

from .db._base import _Land
from .db._enclosed import BIZCALENDARPATH, Path
from .db.misc import find_land_from, lazy_date

CN_BIZDAY_CALENDAR_PATH = "/home/htao_wsl/DATABASE/sina_bizday_calendar.txt"


class MoxCalendar:
    # def __init__(self, land_path) -> None:
    #     path = Path.aspath(land_path)
    #     if not path.exists():
    #         path = find_land_from(path, BIZCALENDARPATH)
    #         if path is None:
    #             raise ValueError(f"Can not find Calendar with name or path<{land_path}>")
    #     super().__init__(path)

    def __init__(self, calendar_path=None) -> None:
        calendar_path = calendar_path or CN_BIZDAY_CALENDAR_PATH
        path = Path.aspath(calendar_path)
        if path.endswith(".npy"):
            raise NotImplemented
        else:
            with open(path) as f:
                self._calendar = cal = np.array(f.read().split("\n"), dtype=int)
        assert (cal[1:] > cal[:-1]).all()

    def next(self, date):
        pass

    def prev(self, date):
        pass

    def range(self, st, ed=None):
        # dates = np.load(self._path.join("dates.npy"))
        cal = self._calendar
        st = np.searchsorted(cal, int(st))
        ed = None if ed is None else np.searchsorted(cal, int(ed))
        return self._calendar[st:ed]

    def get_cache(self, key):
        path = self._path.extend("cache", f"{key}.npy")
        return np.load(path)

    def __contains__(self, d):
        return int(d) in self._calendar
