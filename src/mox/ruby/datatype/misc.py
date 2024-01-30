import re
from .globals import MANA_LIBRARY


def get_default_variable_name(prefix="_x"):
    seq = (
        max(
            [
                int(x[len(prefix) :])
                for x in MANA_LIBRARY.keys()
                if re.match(rf"{prefix}\d+$", x)
            ]
            + [-1]
        )
        + 1
    )

    return prefix + str(seq)
