from dataclasses import dataclass
from types import MappingProxyType
from typing import Dict

import numpy as np

from mox.ruby.datatype import Mana
from mox.ruby.misc import make_tuple


@dataclass
class ManaPoolSchema:
    dates: np.ndarray
    times: np.ndarray
    securities: np.ndarray
    manas: dict


class ManaPool:
    def __init__(self, schema: ManaPoolSchema, manas: Dict[str, Mana]):
        # TODO: future deprecated by user-filepath and to independent os
        self._schema = schema
        self._manas = manas

    @property
    def schema(self):
        # TODO: parse schema to be more clear
        return MappingProxyType(self._schema)

    @property
    def dates(self):
        return self._schema.dates.view()

    @property
    def times(self):
        return self._schema.times.view()

    @property
    def securities(self):
        return self._schema.securities.view()

    @property
    def manas(self):
        return tuple(self._manas.keys())

    @property
    def shape(self):
        tmp_var = self._schema
        return len(tmp_var.dates), len(tmp_var.times), len(tmp_var.securities)

    def depict(self, mana_names=None):
        mana_names = make_tuple(mana_names, fill=self.manas)
        for mn in mana_names:
            print(f"{mn:<17}:{'/r' if len(mn)<20 else '/n'}{' '*20}{self._manas[mn].expr}")

    def __getitem__(self, key):
        return self._manas[key].reshape(self.shape)

    def __setitem__(self, key, value):
        assert isinstance(value, Mana), f"Only Mana can be set in Land, got {type(value)}"
        assert key not in self._manas, f"key<{key}> exists in land, set it in a normal explicit way for safety"
