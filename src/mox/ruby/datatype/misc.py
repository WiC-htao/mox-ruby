import re
from .globals import MANA_LIBRARY, VARIABLE_COUNTER


# def get_variable_no():
#     variable_no_counter = {}
#     prefix, starts = yield
#     while True:
#         if prefix in variable_no_counter:
#             next_no = max(starts, variable_no_counter[prefix]) + 1
#             variable_no_counter[prefix] = next_no
#         else:
#             next_no = variable_no_counter.setdefault(prefix, starts + 1)
#         yield next_no


def get_default_variable_name(prefix="_x"):
    seq = (
        max(
            [int(x[len(prefix) :]) for x in MANA_LIBRARY.keys() if re.match(rf"{prefix}\d+$", x)]
            + [VARIABLE_COUNTER.get(prefix, -1)]
        )
        + 1
    )

    VARIABLE_COUNTER[prefix] = seq

    return prefix + str(seq)
