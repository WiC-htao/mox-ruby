import os
import re
from typing import Self


class Path(str):
    def __new__(cls, path: str, *, is_dir=None) -> None:
        path = os.path.expanduser(path=path)
        if is_dir is None:
            if os.path.isdir(path):
                is_dir = True
        elif os.path.exists(path):
            assert (
                not os.path.isdir(os.path.expanduser(path)) ^ is_dir
            ), f"<{path}> is an existing path, but not consistent with arg<is_dir>={is_dir}"

        if is_dir:
            path = cls._explicit_dir(path)
        path = cls._standardize(path)

        return super().__new__(cls, path)

    def is_dir(self) -> bool:
        return self.endswith("/")

    @property
    def concretize(self, **kwargs) -> Self:
        path: str = re.sub(r"(?<!=%)%(?!%)[^%](?<!%)%(?!%)", lambda x: kwargs.get(x[1:-1], x), self).replace("%%", "%")
        assert (
            "%" not in path
        ), r"SyntaxError of using %UserVar% in Path, unmatched %. Escape character of '%' is \"%%\""
        return self.__class__(path)

    def extend(self, *args) -> Self:
        if len(args) == 0:
            return self
        _other = args[0]
        if os.path.exists(self):
            assert self.is_dir(), "only dir can be extended to a new path"
            return self.__class__(self + _other, is_dir=True).extend(args[1:])
        return self.__class__(self._standardize("/".join((args))))

    @classmethod
    def _explicit_dir(cls, x: str):
        return re.sub(r"/*$", r"/$", x)

    @classmethod
    def _standardize(cls, x: str):
        return re.sub(r"(?<!:)//", "/", x)
