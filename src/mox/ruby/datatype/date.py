import numpy as np


class Date(np.datetime64):
    """Unable used for np.datetime64 can not be heirated, should change in cython"""

    # def __new__(cls, *args, **kwargs):
    #     obj = np.datetime64.__new__(cls, *args, **kwargs)
    #     obj.__class__ = cls
    #     return obj

    # def __init__(self, *args, **kwargs):
    #     assert self.dtype == np.dtype("<M8[D]")

    @property
    def year(self):
        return self.astype("datetime64[Y]").astype(int) + 1970

    @property
    def month(self):
        return self.astype("datetime64[M]").astype(int) % 12 + 1

    @property
    def day(self):
        return self - self.astype("datetime64[M]") + 1


# class Time:
#     """
#     I think i can use a int64 to present a ns from 00:00:00,
#     and changed to np.timedelta64 when calculate with Date above.
#     But i think both of them need to be extended with in C-numpy to
#     keep a apparent str present in an array
#     """
