from dataclasses import dataclass
from types import MappingProxyType
from typing import Dict

import numpy as np

from ._enclosed import Mana, make_tuple


@dataclass
class ManaIndexer:
    date: np.ndarray
    time: np.ndarray
    security: np.ndarray


class ManaPool:
    def __init__(self, indexer: ManaIndexer, manas: Dict[str, Mana]):
        # TODO: future deprecated by user-filepath and to independent os
        self._indexer = indexer
        self._manas = manas

    @property
    def indexer(self):
        # TODO: parse schema to be more clear
        return MappingProxyType(self._indexer)

    @property
    def dates(self):
        return self._indexer.date.view()

    @property
    def times(self):
        return self._indexer.time.view()

    @property
    def securities(self):
        return self._indexer.security.view()

    @property
    def manas(self):
        return tuple(self._manas.keys())

    @property
    def shape(self):
        tmp_var = self._indexer
        return len(tmp_var.date), len(tmp_var.time), len(tmp_var.security)

    def depict(self, mana_names=None):
        mana_names = make_tuple(mana_names, fill=self.manas)
        for mn in mana_names:
            print(f"{mn:<17}:{'/r' if len(mn)<20 else '/n'}{' '*20}{self._manas[mn].expr}")

    def __getitem__(self, key):
        return self._manas[key].reshape(self.shape)

    def __setitem__(self, key, value):
        assert isinstance(value, Mana), f"Only Mana can be set in Land, got {type(value)}"
        assert key not in self._manas, f"key<{key}> exists in land, set it in a normal explicit way for safety"

    def which(self):
        pass

    def get_df(self):
        pass

    def get_field_df(self, field):
        pass
