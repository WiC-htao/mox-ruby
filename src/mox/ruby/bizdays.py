from typing import Self
import numpy as np

from pathlib import Path


class Bizdays:
    # def __init__(self, land_path) -> None:
    #     path = Path.aspath(land_path)
    #     if not path.exists():
    #         path = find_land_from(path, BIZCALENDARPATH)
    #         if path is None:
    #             raise ValueError(f"Can not find Calendar with name or path<{land_path}>")
    #     super().__init__(path)

    # def __init__(self, calendar_path=None) -> None:
    #     calendar_path = calendar_path or CN_BIZDAY_CALENDAR_PATH
    #     path = Path.aspath(calendar_path)
    #     if path.endswith(".npy"):
    #         raise NotImplementedError
    #     with open(path, encoding="UTF8") as f:
    #         self._calendar = cal = np.array(f.read().split("\n"), dtype=int)
    #     assert (cal[1:] > cal[:-1]).all()
    #     self._path = path
    def __init__(self, bizdays):
        self.bizdays = bizdays

    @staticmethod
    def read_dts(path) -> np.ndarray:
        with open(path, "r") as f:
            dates = f.readlines()
        return np.array(dates, dtype=np.int32)

    @staticmethod
    def assert_monotonicity(array, strict=False, descending=False):
        order_relationship = (np.greater, np.greater_equal, np.less, np.less_equal)[2 * descending + strict]
        assert order_relationship(array[1:], array[:-1]).all()

    @classmethod
    def from_dts(cls, path) -> Self:
        bizdays = cls.read_dts(path)
        cls.assert_monotonicity(bizdays)
        return cls(bizdays)

    def next(self, date):
        idx = np.searchsorted(self.bizdays, date, side="right")
        return self.bizdays[idx]

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

    # def __init__(self, calendar_path=None) -> None:
    #     calendar_path = calendar_path or CN_BIZDAY_CALENDAR_PATH
    #     path = Path.aspath(calendar_path)
    #     if path.endswith(".npy"):
    #         raise NotImplementedError
    #     with open(path, encoding="UTF8") as f:
    #         self._calendar = cal = np.array(f.read().split("\n"), dtype=int)
    #     assert (cal[1:] > cal[:-1]).all()
    #     self._path = path
