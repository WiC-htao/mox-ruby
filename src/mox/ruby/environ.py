import os
from pathlib import Path

# from mox.ruby.datatype import Path


UNIV_DIR = [
    Path(p, is_dir=True) for p in os.environ.get("UNIV_DIR", "").split(":") if p
]

BIZCALENDAR_DIR = [
    Path(p, is_dir=True) for p in os.environ.get("BIZ_CALENDAR_DIR", "").split(":") if p
]
