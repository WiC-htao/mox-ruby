from dataclasses import dataclass, asdict
from typing import Dict

import numpy as np

from ._enclosed import Mana, make_tuple


@dataclass(slots=True)
class ManaIndexer:
    date: np.ndarray
    time: np.ndarray
    ukey: np.ndarray


class ManaPool:
    def __init__(self, indexer: ManaIndexer, manas: Dict[str, Mana]):
        # TODO: future deprecated by user-filepath and to independent os
        self._indexer = indexer
        self._manas = manas

    @property
    def indexer(self):
        # TODO: parse schema to be more clear
        return asdict(self._indexer)

    @property
    def dates(self):
        return self._indexer.date.view()

    @property
    def times(self):
        return self._indexer.time.view()

    @property
    def ukeys(self):
        return self._indexer.ukey.view()

    @property
    def manas(self):
        return tuple(self._manas.keys())

    @property
    def shape(self):
        _idx = self._indexer
        return len(_idx.date), len(_idx.time), len(_idx.ukey)

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
