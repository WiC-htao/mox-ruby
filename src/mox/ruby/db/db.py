from types import MappingProxyType
from mox.ruby.misc import load_yaml


class Db:
    def __init__(self, db_path):
        # TODO: future deprecated by user-filepath and to independent os
        if not db_path.endswith("/"):
            db_path = db_path.join("/")

        self._db = db_path
        self._structure = load_yaml(db_path + ".structure.yaml")

    @property
    def structure(self):
        # TODO: parse schema to be more clear
        return MappingProxyType(self._structure)

    def get_data(self):
        pass
