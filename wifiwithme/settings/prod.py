# You must set a customized an non versioned SECRET_KEY in production mode

DEBUG = False
SECRET_KEY = None

try:
    from .local import *
except ImportError:
    pass

from .base import *
