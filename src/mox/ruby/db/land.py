import itertools

from ._base import _Land
from .calendar import Calendar
from .univ import Univ


class Land(_Land):
    def __init__(self, land_path) -> None:
        super().__init__(land_path)
        self._univ = Univ(self.schema["univ"])
        self._calendar = Calendar(self.schema["calendar"])

    def get_mana(self):
        pass

        # for concretize_args in dict_product(direct_cache_idx):
        #     path = self._path.extend(cache_info["path"]).concretize(**{k: kwargs[k] for k in cache_info["require"]})


def dict_product(d):
    keys = d.keys()
    values = itertools.product(*d.values())
    for v in values:
        yield dict(zip(keys, v))

