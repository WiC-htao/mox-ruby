from types import MappingProxyType

import numpy as np

symbol_priority = MappingProxyType({"+": 0, "/": 1})

ufunc_mapping = MappingProxyType({np.add: "+", np.divide: 1})

symbol_priority_list = (("+", "-"), ("/", "*"))
# date0 = np.datetime64("1970-01-01")

str_value_map = MappingProxyType({"nan": np.nan})


TIME_CONST = {"ch_eod": "20:00:00",'ch_sod':"07:00:00"}
