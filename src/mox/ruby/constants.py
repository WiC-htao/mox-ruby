"""
constants during running
"""

from pathlib import Path
import os
from .database import DB_API

DATABASE_PATH = Path(os.environ.get("DATABASE_PATH", os.path.abspath("~/DATABASE")))

RUNNING_TYPE = os.environ.get("MOX_RUBY_RUNNING_TYPE", "PROD")

DATABASE = DB_API(DATABASE_PATH)
