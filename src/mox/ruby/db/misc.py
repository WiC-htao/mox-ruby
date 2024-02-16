import numpy as np


def find_land_from(land, libs):
    for lib in libs:
        if land in lib.listdir():
            return lib.extend(land)
    return None


def lazy_date(date):
    date = str(date)
    if len(date) == 8:
        return np.datetime64(f"{date[:4]}-{date[4:6]}-{date[6:]}")
    else:
        return np.datetime64(date, dtype=f"datetime64[D]")
