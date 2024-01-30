from typing import Any, Literal
import numpy as np
from .globals import MANA_LIBRARY
from .misc import get_default_variable_name


def mana(*args, expr=None, prefix=None, **kwargs):
    ret = np.array(*args, **kwargs).view(Mana)
    if expr is None:
        expr = get_default_variable_name(prefix)
    elif expr:
        assert expr not in MANA_LIBRARY
    MANA_LIBRARY[expr] = ret
    ret.expr = expr
    return ret


class Mana(np.ndarray):
    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        obj.expr = None
        return obj

    def __array_ufunc__(
        self,
        ufunc: np.ufunc,
        method: Literal[
            "__call__", "reduce", "reduceat", "accumulate", "outer", "inner"
        ],
        *inputs: Any,
        **kwargs: Any,
    ) -> Any:
        output_shape = np.broadcast_shapes(*(i.shape for i in inputs))
        output = Mana(output_shape)
        super().__array_ufunc__(ufunc, method, *inputs, out=output, **kwargs)
        if ufunc is np.add and len(kwargs) == 0:
            output.expr = " + ".join(input.expr for input in inputs)
        else:
            output.expr = (
                ufunc.__name__ + "(" + ",".join(input.expr for input in inputs) + ")"
            )
        MANA_LIBRARY[output.expr] = output
        return output
