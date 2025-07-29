import os
import warnings
from typing import Dict, Iterable, Tuple

import numpy as np
import yaml


def load_yaml(path) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def dump_yaml(dt, path) -> None:
    assert not os.path.exists(path), f"File<{path}> exists. Use overwrite_yaml instead"
    with open(path, "w", encoding="utf-8") as f:
        return yaml.safe_dump(dt, f)


def overwrite_yaml(dt, path) -> None:
    if not os.path.exists(path):
        warnings.warn(
            f"File<{path}> not exists. Encourage using dump_yaml instead to be more safety"
        )
    with open(path, "w", encoding="utf-8") as f:
        return yaml.safe_dump(dt, f)


def make_tuple(x, split_array=True) -> Tuple:
    if isinstance(x, Iterable) and not isinstance(
        x, str if split_array else (str, np.ndarray)
    ):
        return tuple(x)
    return (x,)


class VoidClass:  # pylint: disable=too-few-public-methods
    def __new__(cls) -> None:
        raise TypeError("VoidClass can't instantiate")

    def __init_subclass__(cls) -> None:
        raise TypeError("VoidClass can't be inherited")
