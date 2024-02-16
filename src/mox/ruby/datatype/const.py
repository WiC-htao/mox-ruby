from types import MappingProxyType

import numpy as np

symbol_priority_mapping = MappingProxyType({"+": 0, "/": 1})

binary_ufunc_symbol_mapping = MappingProxyType({np.add: "+", np.divide: "/"})

symbol_list_by_priority = (("+", "-"), ("/", "*"))

reversed_symbol = {"/", "-"}
