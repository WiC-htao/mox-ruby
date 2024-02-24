import re
from types import MappingProxyType
from typing import Dict

import numpy as np

from ._enclosed import TIME_CONST, Mana, Path, load_yaml, make_tuple
from .const import DIRECT
from .manapool import ManaIndexer, ManaPool


class _Land:
    # pylint: disable=too-few-public-methods

    def __init__(self, land_path) -> None:

        self._path = Path.aspath(path=land_path)
        self._schema: Dict = load_yaml(path=self._path.extend(".structure.yaml"))
        self._schema["name"] = re.search(r"/(?P<name>.*)/$", self._path).group("name")
        assert "asset" in self._schema
        self._univ = self._calendar = None

    @property
    def schema(self) -> MappingProxyType:
        # TODO: parse schema to be more clear
        return MappingProxyType(mapping=self._schema)

    def __repr__(self):
        return f"{self.__class__.__name__}<{self._schema['name']}> of {self._schema['asset']} at {self._path}"

    def _get_mana_from_cache_info(self, cache_info, **kwargs):
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

        manas = {}
        if cache_info["field"] == DIRECT:
            field = make_tuple(kwargs["field"])
            for f in field:
                path = self._path.extend((cache_info["path"])).concretize(field=f)
                fmana = np.load(path).view(Mana)
                fmana.expr = self.schema["field"][f]["expr"]
                manas[f] = fmana
        else:
            cluster_mana = np.load(self._path.extend((cache_info["path"])))
            fields = make_tuple(cache_info["field"])
            if len(fields) == 1:
                manas = {fields[0]: cluster_mana.view(Mana)}
            else:
                manas = {f: m.view(Mana) for f, m in zip(fields, cluster_mana)}

        indexer = ManaIndexer(date, time, security)
        return ManaPool(indexer, manas)
