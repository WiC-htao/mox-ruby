from typing import Iterable, Tuple

import numpy as np


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
