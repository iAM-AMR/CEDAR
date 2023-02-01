

# DEVELOPMENT SETTINGS

# This file imports base settings, and applies development settings. Use of 
# the development environment requires specifying database connection parameters, 
# in ../settings_local.py. See ../settings_local_example.py


import os

# Try base settings import; error if fail.

try:
    from .base_settings import *
except ImportError as error_development_import_settings_base:
    pass

# Try local settings import; error if fail.

try:
    from .local_settings import *
except ImportError as error_local_settings:
    pass


# DEBUG is specified using an environment variable, and should be False in production.

DEBUG = True

# When DEBUG is True and ALLOWED_HOSTS is empty, the host is validated against
# ['.localhost', '127.0.0.1', '[::1]']. 
# See https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts

ALLOWED_HOSTS = []

# This key is not secret.
SECRET_KEY = '#4-0mz6rs$&b)8h5zmam!8*87q6-#fck$$^r47xdwh0ri5b5&!'



# STATIC FILES
# -------------------------------------

# See comments in base settings re: static files. The following are defined
# in base settings:
#  - STATIC_URL (the URL to use when referring to static files located in STATIC_ROOT)

# STATIC_ROOT is the absolute path to the directory where collectstatic() will 
# collect static files for deployment. See 
# https://docs.djangoproject.com/en/4.1/ref/contrib/staticfiles/#collectstatic

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# STATICFILES_STORAGE



# Fail loudly
CRISPY_FAIL_SILENTLY = False
