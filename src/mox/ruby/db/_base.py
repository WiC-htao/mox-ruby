import re
from types import MappingProxyType
from typing import Dict

from ._enclosed import Path, load_yaml


class _Lands:
    # pylint: disable=too-few-public-methods

    def __init__(self, land_path) -> None:

        self._path = Path.aspath(path=land_path)
        self._schema: Dict = load_yaml(path=self._path.extend(".structure.yaml"))
        self._schema["name"] = re.search(r"/(?P<name>.*)/$", self._path).group("name")

    @property
    def schema(self) -> MappingProxyType:
        # TODO: parse schema to be more clear
        return MappingProxyType(mapping=self._schema)

    def __repr__(self):
        return f"{self.__class__.__name__}<{self._schema['name']}> of {self._schema['univ']} at {self._path}"
