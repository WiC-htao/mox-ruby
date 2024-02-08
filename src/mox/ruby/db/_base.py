from types import MappingProxyType
from typing import Dict

from mox.ruby.datatype import Path
from mox.ruby.misc import load_yaml


class _Lands:
    # pylint: disable=too-few-public-methods

    def __init__(self, land_path) -> None:

        self._path = Path(path=land_path)
        self._structure: Dict = load_yaml(path=self._path.join(".structure.yaml"))

    @property
    def structure(self) -> MappingProxyType:
        # TODO: parse schema to be more clear
        return MappingProxyType(mapping=self._structure)

    def _get_cache(self, **kwargs):
        pass

    def _build_schema(self):
        pass
