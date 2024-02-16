import os

from mox.ruby.datatype import Path

UNIVPATH = [Path(p, is_dir=True) for p in os.environ.get("UNIVPATH", "").split(":") if p]

CALENDARPATH = [Path(p, is_dir=True) for p in os.environ.get("CALENDARPATH", "").split(":") if p]
