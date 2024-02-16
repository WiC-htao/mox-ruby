import re
from typing import Any, Literal

import numpy as np
from numpy._typing import NDArray

from .const import (binary_ufunc_symbol_mapping, reversed_symbol,
                    symbol_list_by_priority, symbol_priority_mapping)
from .globals import MANA_LIBRARY
from .misc import get_default_variable_name


def mana(*args, expr=None, prefix="_x", **kwargs):
    ret = np.array(*args, **kwargs).view(Mana)
    if expr is None:
        expr = get_default_variable_name(prefix)
    elif expr:
        assert expr not in MANA_LIBRARY
    MANA_LIBRARY[expr] = ret
    ret.expr = expr
    return ret


class Mana(np.ndarray):
    def __array_finalize__(self, obj: NDArray[Any] | None) -> None:
        self.expr = getattr(obj, "expr", None)  # pylint: disable=attribute-defined-outside-init

    def __array_ufunc__(
        self,
        ufunc: np.ufunc,
        method: Literal["__call__", "reduce", "reduceat", "accumulate", "outer", "inner"],
        *inputs: Any,
        out=None,
        **kwargs: Any,
    ) -> Any:
        """recoding each ufunc operation"""
        # output_shape = np.broadcast_shapes(*(i.shape for i in inputs))
        # output = Mana(output_shape)
        ndarray_inputs = [i.view(np.ndarray) if isinstance(i, np.ndarray) else i for i in inputs]

        if out is None:
            outputs = None
        else:
            if ufunc.nout == 1:
                out = (out,)
            outputs = tuple(ot.view(np.ndarray) for ot in outputs)

        results = getattr(ufunc, method)(*ndarray_inputs, out=outputs, **kwargs)
        if out is None:
            outputs = results = (
                (np.asarray(results).view(Mana),)
                if ufunc.nout == 1
                else tuple(np.asarray(r).view(Mana) for r in results)
            )
        inputs_expr = tuple(inpt.expr if hasattr(inpt, "expr") else str(inpt) for inpt in inputs)
        for i, output in enumerate(outputs):
            if not isinstance(output, Mana):
                continue
            old_expr = output.expr
            if ufunc in binary_ufunc_symbol_mapping.keys() and len(kwargs) == 0:
                symbol = binary_ufunc_symbol_mapping[ufunc]
                output.expr = auto_bracket_binary(inputs_expr, symbol)
            else:
                output.expr = ufunc.__name__ + (f"_{i}(" if len(outputs) > 1 else "(") + ",".join(inputs_expr) + ")"
            if old_expr:
                del MANA_LIBRARY[old_expr]
            MANA_LIBRARY[output.expr] = output
        return results if ufunc.nout > 1 and len(results) > 1 else results[0]


def auto_bracket_binary(inputs, symbol):

    symbol_priority = symbol_priority_mapping[symbol]
    return (
        (
            bracket(inputs[0])
            if find_freesymbol(inputs[0], sum(symbol_list_by_priority[:symbol_priority], start=()))
            else inputs[0]
        )
        + f" {symbol} "
        + (
            bracket(inputs[1])
            if find_freesymbol(
                inputs[0],
                sum(symbol_list_by_priority[: symbol_priority + int(symbol_priority in reversed_symbol)], start=()),
            )
            else inputs[1]
        )
    )

    # symbol_priority = symbol_priority_mapping[symbol]
    # symbol_list = symbol_list_by_priority[: symbol_priority + int(symbol in reversed_symbol)]
    # free_symbol_1 = find_freesymbol(inputs[1], symbol_list)
    # if free_symbol_1:
    #     latter = bracket(inputs[1])


def bracket(x):
    return f"({x})"


def find_freesymbol(expr, symbol_list):
    if len(symbol_list) == 0:
        return []
    while "(" in expr:
        expr = re.sub(r"\([^\(\)]*\)", "_x", expr)
    return [symbol for symbol in symbol_list if symbol in expr]
