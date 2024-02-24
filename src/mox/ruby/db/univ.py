import numpy as np

from ._base import _Land
from ._enclosed import UNIVPATH, Path
from .calendar import Calendar
from .misc import find_land_from


class Univ(_Land):
    def __init__(self, land_path) -> None:
        path = Path.aspath(land_path)
        if not path.exists():
            path = find_land_from(path, UNIVPATH)
            if path is None:
                raise ValueError(f"Can not find Univ with name or path<{land_path}>")
        super().__init__(path)
        self._calendar = Calendar(self._schema["calendar"])
        self._univ = self

    def get_ids(self, date):
        pass

    def get_id_union(self, dates=None, start=None, end=None):
        assert start or end or dates is not None

    def get_cache(self, key):
        cache_info = self.schema["cache"][key]
        if cache_info["type"] == "security":
            return np.load(self._path.extend(cache_info["path"]))
        if cache_info["type"] == "mana":
            cache_info = cache_info.copy()
            cache_info["field"] = key
            return self._get_mana_from_cache_info(cache_info)
        raise NotImplementedError
