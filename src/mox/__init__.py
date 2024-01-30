import pkgutil

pkgutil.extend_path(__path__, __name__)

from .datatypes import mana, Mana, get_default_variable_name, MANA_LIBRARY
