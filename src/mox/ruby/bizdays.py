from typing import Self

import numpy as np


class Bizdays:
    def __init__(self, bizdays):
        self.assert_monotonicity(bizdays, strict=True)
        self.bizdays = bizdays

    @staticmethod
    def read_dts(path) -> np.ndarray:
        with open(path, "r") as f:
            dates = f.readlines()
        return np.array(dates, dtype=np.int32)

    @staticmethod
    def assert_monotonicity(array, strict=False, descending=False):
        order_relationship = (np.greater_equal, np.greater, np.less_equal, np.less)[
            2 * descending + strict
        ]
        assert order_relationship(array[1:], array[:-1]).all()

    @classmethod
    def from_dts(cls, path) -> Self:
        bizdays = cls.read_dts(path)
        return cls(bizdays)

    def next(self, date):
        idx = np.searchsorted(self.bizdays, date, side="right")
        return self.bizdays[idx]

    def prev(self, date):
        idx = np.searchsorted(self.bizdays, date, side="left")
        if idx == 0:
            raise ValueError(f"no days before <date>, {date} ")
        return self.bizdays[idx - 1]

    def range(self, sd=None, ed=None):
        bizdays = self.bizdays
        sd_idx = np.searchsorted(bizdays, int(sd), side="left")
        ed_idx = None if ed is None else np.searchsorted(bizdays, int(ed), side="right")
        return bizdays[sd_idx:ed_idx]

    def get_cache(self, key):
        path = self._path.extend("cache", f"{key}.npy")
        return np.load(path)

    def __contains__(self, d):
        return int(d) in self.bizdays
