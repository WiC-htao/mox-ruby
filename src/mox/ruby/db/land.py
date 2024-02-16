import itertools

import numpy as np

from mox.ruby.datatype.mana import Mana

from ._base import _Lands
from ._enclosed import TIME_CONST, make_tuple
from .calendar import Calendar
from .const import DIRECT
from .manapool import ManaIndexer, ManaPool
from .univ import Univ


class Land(_Lands):
    def __init__(self, land_path) -> None:
        super().__init__(land_path)
        self._univ = Univ(self.schema["univ"])
        self._calendar = Calendar(self.schema["calendar"])

    def get_mana(self):
        pass

    def _get_unit_cache(self, name, **kwargs):
        cache_info = self.schema["unit_cache"][name]
        # direct_cache_idx = {}
        date = cache_info.get("date", self.schema["indexer"]["date"])
        if isinstance(date, dict) and date.get("type") == "compact:cache":
            date = self._calendar.get_cache(date["name"])

        time = cache_info.get("time", self.schema["indexer"]["time"])
        if isinstance(time, str) and not time.startswith("!"):
            time = make_tuple(TIME_CONST[time])

        security = cache_info.get("security", self.schema["indexer"]["security"])
        if isinstance(security, dict) and security.get("type") == "compact:cache":
            security = self._univ.get_cache(security["name"])

        if cache_info["field"] == DIRECT:
            field = make_tuple(kwargs["field"])
            direct_field = True

        manas = {}
        if direct_field:
            for f in field:
                path = self._path.extend((cache_info["path"])).concretize(field=f)
                fmana = np.load(path).view(Mana)
                fmana.expr = self.schema["field"][f]["expr"]
                manas[f] = fmana
        else:
            raise NotImplementedError
        indexer = ManaIndexer(date, time, security)
        return ManaPool(indexer, manas)
        # for concretize_args in dict_product(direct_cache_idx):
        #     path = self._path.extend(cache_info["path"]).concretize(**{k: kwargs[k] for k in cache_info["require"]})


def dict_product(d):
    keys = d.keys()
    values = itertools.product(*d.values())
    for v in values:
        yield dict(zip(keys, v))
