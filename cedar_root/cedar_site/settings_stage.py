


from pathlib import Path
import os

try:
    from .settings import *
except ImportError as error_local_settings:
    pass


ALLOWED_HOSTS = []

DEBUG = True

SECRET_KEY = '#4-0mz6rs$&b)8h5zmam!8*87q6-#fck$$^r47xdwh0ri5b5&!'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    BASE_DIR / 'cedar_site/static'
]

# STATICFILES_STORAGE

try:
    from .settings_local import *
except ImportError as error_local_settings:
    pass

