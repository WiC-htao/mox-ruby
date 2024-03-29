import os
import re
from typing import List, Self, Union


class Path(str):
    def __new__(cls, path: str, *, is_dir=None) -> None:
        path = os.path.expanduser(path=path.strip())
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

    def listdir(self) -> List[str]:
        return os.listdir(self)

    def exists(self) -> bool:
        return os.path.exists(self)

    def concretize(self, **kwargs) -> Self:
        def _sub(x):
            return kwargs.get(x.group()[1:-1], x.group())

        path: str = re.sub(r"(?<!=%)%(?!%)[^%]*(?<!%)%(?!%)", _sub, self).replace("%%", "%")
        assert (
            "%" not in path
        ), r"SyntaxError of using %UserVar% in Path, unmatched %. Escape character of '%' is \"%%\""
        return self.__class__(path)

    def extend(self, *args) -> Self:
        if len(args) == 0:
            raise ValueError("nothing to extend")
        if os.path.exists(self):
            assert self.is_dir(), "only dir can be extended to a new path"
            if len(args) > 1:
                return self.__class__(self + args[0], is_dir=True).extend(*args[1:])
            return self.__class__(self + args[0], is_dir=None)
        return self.__class__(self._standardize("/".join((self,) + args)))

    @classmethod
    def _explicit_dir(cls, x: str):
        return re.sub(r"/*$", r"/", x)

    @classmethod
    def _standardize(cls, x: str):
        return re.sub(r"(?<!:)//", "/", x)

    @classmethod
    def aspath(cls, path: Union[str, Self], *, is_dir=None):
        if isinstance(path, Path) and (path.is_dir == is_dir or is_dir is None):
            return path
        return cls(path, is_dir=is_dir)
