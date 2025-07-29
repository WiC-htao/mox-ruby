from .const import DATABASE_CONSTANTS_FILE
from .misc import load_yaml
from pathlib import Path
from typing import Union, Tuple


class DB_API:
    BIZDAYS_DIR = "bizdays"

    def __init__(self, db_path: Path):
        self._path = db_path
        self._constants = load_yaml(
            DATABASE_CONSTANTS_FILE.join(DATABASE_CONSTANTS_FILE)
        )

    @property
    def constants(self):
        return self._constants

    def get_bizdays(self, key: Union[str, Tuple[str]]):
        key = self.parse_key_alias(key) if isinstance(key, str) else key
        filename = self.constants["BIZDAYS"]
        for k in key:
            filename = filename[k]
        filepath = self.extend_path(self.BIZDAYS_DIR, filename)
        return Bizdays.from_dts(filepath)

    def _extend_path(self, *paths) -> Path:
        path = self._path
        for pth in paths:
            path = path.join(pth)
        return path

    @staticmethod
    def parse_key_alias(key_alias):
        return key_alias.split(".")
