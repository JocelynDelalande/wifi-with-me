try:
    from .local import *
except ImportError:
    pass

from .base import *

DEBUG = True
INSTALLED_APPS += [
    'debug_toolbar',
]
