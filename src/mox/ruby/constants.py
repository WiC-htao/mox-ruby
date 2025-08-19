"""
constants during running
"""

import os
from pathlib import Path

from .database import DB_API

DATABASE_PATH = Path(os.environ.get("DATABASE_PATH", "~/DATABASE")).expanduser()

RUNNING_TYPE = os.environ.get("RUBY_RUNNING_TYPE", "PROD")

DATABASE = DB_API(DATABASE_PATH)
