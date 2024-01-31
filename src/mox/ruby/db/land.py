from mox.ruby.datatype import Mana
from mox.ruby.misc import load_yaml
from types import MappingProxyType


class Land:
    def __init__(self, schema, manas):
        # TODO: future deprecated by user-filepath and to independent os
        self._schema = schema
        self._manas = manas

    @property
    def schema(self):
        # TODO: parse schema to be more clear
        return MappingProxyType(self._schema)

    @property
    def dates(self):
        pass

    @property
    def times(self):
        pass

    @property
    def securities(self):
        pass

    @property
    def shape(self):
        pass

    def __getitem__(self, key):
        return self._manas[key].reshape(self.shape)

    def __setitem__(self, key, value):
        assert isinstance(
            value, Mana
        ), f"Only Mana can be set in Land, got {type(value)}"
        assert (
            key not in self._manas
        ), f"key<{key}> exists in land, set it in a normal explicit way for safety"
