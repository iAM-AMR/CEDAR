

# PRODUCTION SETTINGS

# This file imports base settings and applies production settings (deployed on
#  Azure App Service).



import os

# Try base settings import; error if fail.

try:
    from .base_settings import *
except ImportError as error_production_import_settings_base:
    pass




# If DEBUG is False, you also need to properly set the ALLOWED_HOSTS setting. 
# Failing to do so will result in all requests being returned as “Bad Request (400)”.
# See https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts

DEBUG = [os.environ['DEBUG']] == 'TRUE'


# We set WEBSITE_HOSTNAME on Azure App Service. If missing, set an empty
# ALLOWED_HOSTS to return bad requests.

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []


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
