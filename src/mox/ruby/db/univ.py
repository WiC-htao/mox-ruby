import numpy as np

from ._base import _Lands
from ._enclosed import UNIVPATH, Path
from .misc import find_land_from


class Univ(_Lands):
    def __init__(self, land_path) -> None:
        path = Path.aspath(land_path)
        if not path.exists():
            path = find_land_from(path, UNIVPATH)
            if path is None:
                raise ValueError(f"Can not find Univ with name or path<{land_path}>")
        super().__init__(path)

    def get_cache(self, key):
        cache_info = self.schema["cache"][key]
        if cache_info["type"] == "security":
            return np.load(self._path.extend(cache_info["path"]))
        raise NotImplementedError
