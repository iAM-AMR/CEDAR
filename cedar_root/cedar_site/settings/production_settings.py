
"""
Production Settings
"""

# A Django settings file contains the configuration of the Django installation.
# There are multiple CEDAR settings files - this is the PRODUCTION SETTINGS file.

# These settings are used in production. 
# This file imports SETTINGS_BASE.

# The command pythonmanage.pydiffsettingsdisplays differences between the current 
# settings file and Django’s default settings.


import os

# Try base settings import; error if fail.

try:
    from .base_settings import *
except ImportError as error_production_import_settings_base:
    pass



# DEBUG is specified using an environment variable, and should be False in production.

# Environment variables are read as strings, but DEBUG must be set using a boolean. So 
# create a boolean from the string by evaluating the equality of 'true' and the contents 
# of environment variable DEBUG (which returns 'False' if not specified). Use .lower to
# ensure true, True, and TRUE are equivalent. 

DEBUG = (os.getenv('DEBUG', default = 'False').lower() == 'true')



# ALLOWED_HOSTS is list of strings representing the host/domain names that this 
# Django site can serve. Default: [] (Empty list). When DEBUG is True and 
# ALLOWED_HOSTS is empty, the host is validated against ['.localhost', '127.0.0.1', '[::1]'].
# When DEBUG is False, ALLOWED_HOSTS must be set. Else, all requests are returned
# as 400 Bad Requests.

# Environment variable ALLOWED_HOSTS is a string of IP addresses, FQDNs, or 
# '.' wild-cards, seperated by a space.

ALLOWED_HOSTS =  os.environ.get('ALLOWED_HOSTS').split(' ')



# CSRF_TRUSTED_ORIGIN is a list of strings representing the host/domain names
# of trusted origins for unsafe requests (e.g., POST).

# MORE DETAIL HERE

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS').split(' ')



# SECRET_KEY is a salt; it is used for hashing. 

SECRET_KEY = [os.environ['SECRET_KEY']]



# STATIC FILES
# -------------------------------------

# See comments in base settings re: static files. The following are defined
# in base settings:
#  - STATIC_URL (the URL to use when referring to static files located in STATIC_ROOT)

# STATIC_ROOT is the absolute path to the directory where collectstatic() will 
# collect static files for deployment.
# See https://docs.djangoproject.com/en/4.1/ref/contrib/staticfiles/#collectstatic

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')







# --- END PROD/DEV FORMAT PARITY



# DBHOST is only the server name, not the full URL
hostname = os.environ['DBHOST']

# Configure Postgres database; the full username is username@servername,
# which we construct using the DBHOST value.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': hostname + ".postgres.database.azure.com",
        'USER': os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASS'], 
        'OPTIONS': {'sslmode': 'require'}
    }
}
