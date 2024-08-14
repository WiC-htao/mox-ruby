import re
from types import MappingProxyType
from typing import Dict
from mox.ruby.datatype import mana

import numpy as np
import yaml

from ._enclosed import TIME_CONST, Mana, Path, load_yaml, make_tuple, overwrite_yaml
from .const import DIRECT
from .manapool import ManaIndexer, ManaPool


class _Land:
    # pylint: disable=too-few-public-methods

    def __init__(self, land_path) -> None:

        self._path = Path.aspath(path=land_path)
        self._schema: Dict = load_yaml(path=self._path.extend(".schema.yaml"))
        self._schema["name"] = re.search(r"/(?P<name>.*)/$", self._path).group("name")
        assert "asset" in self._schema
        self._univ = None
        self._calendar = None

    @property
    def schema(self) -> MappingProxyType:
        # TODO: parse schema to be more clear
        return MappingProxyType(mapping=self._schema)

    def __repr__(self):
        return f"{self.__class__.__name__}<{self._schema['name']}> of {self._schema['asset']} at {self._path}"

    def _get_mana_from_cache_info(self, cache_info, **kwargs):
        # direct_cache_idx = {}
        date = cache_info["date"]
        if isinstance(date, dict) and date.get("type") == "compact:cache":
            date = self._calendar.get_cache(date["name"])

        time = cache_info.get("time", self._schema["time"])
        if isinstance(time, str) and not time.startswith("!"):
            time = make_tuple(TIME_CONST.get(time, time))
        elif time is None:
            time = self.time

        security = cache_info.get("security")
        if isinstance(security, dict) and security.get("type") == "compact:cache":
            security = self._univ.get_cache(security["name"])

        manas = {}
        if cache_info["field"] == DIRECT:
            fields = make_tuple(kwargs["fields"])
            for f in fields:
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

    def set_mana_cache(self, manapool, cache_key, date_cache_type="calendar_cache", time_cache_type="plain", **kwargs):
        cache_info = {}
        if date_cache_type == "calendar_cache":

            self._calendar.set_cache(manapool.dates, kwargs.get("calendar_cache_key", cache_key))
        else:
            raise NotImplementedError
        if time_cache_type == "plain":
            pass
        # if time_cache_type == ""

    def __overwrite_schema(self):
        pass