
"""
Default Settings
"""

import os

try:
    from .settings_common import *
except ImportError as error_importing_common_deployment_settings:
    pass

# Environment variables are read as strings, but some settings are booleans.
# Create a boolean from a string by evaluating its equality with 'true'. Use 
# .lower to ensure true, True, and TRUE are equivalent. 



# DEBUG is specified using an environment variable, and should be False in production.

DEBUG = (os.getenv('DEBUG', default = 'False').lower() == 'true')

# SECRET_KEY is salt for hashing.

SECRET_KEY = [os.environ['SECRET_KEY']]



# NETWORK
# -----------------------------------------------------------------------------

# ALLOWED_HOSTS is list of strings representing the host/domain names that this 
# Django site can serve. Default: [] (Empty list). When DEBUG is True and 
# ALLOWED_HOSTS is empty, the host is validated against ['.localhost', '127.0.0.1', '[::1]'].
# When DEBUG is False, ALLOWED_HOSTS must be set. Else, all requests are returned
# as 400 Bad Requests.

# Environment variable ALLOWED_HOSTS is a string of IP addresses, FQDNs, or 
# '.' wild-cards, seperated by a comma.

ALLOWED_HOSTS =  os.environ.get('ALLOWED_HOSTS').split(',')


# CSRF_TRUSTED_ORIGIN is a list trusted origins for unsafe requests (e.g. POST).
# For requests that include the Origin header, Django’s CSRF protection requires 
# that header match the origin present in the Host header. For a secure unsafe 
# request that doesn’t include the Origin header, the request must have a Referer 
# header that matches the origin present in the Host header.

# Note, this may not be needed where SECURE_PROXY_SSL_HEADER is set, below, as is_secure()
# should not automatically fail on Azure App Service.

# CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS').split(',')


#  SECURE_PROXY_SSL_HEADER is a tuple representing an HTTP header/value combination 
# that signifies a request is secure. By default, is_secure() determines if a 
# request is secure by confirming that a requested URL uses https://. This method 
# is important for Django’s CSRF protection, and it may be used by your own code 
# or third-party apps. If your Django app is behind a proxy, though, the proxy may
# be “swallowing” whether the original request uses HTTPS or not. In this situation, 
# configure your proxy to set a custom HTTP header that tells Django whether the 
# request came in via HTTPS, and set SECURE_PROXY_SSL_HEADER so that Django knows
# what header to look for. https://docs.djangoproject.com/en/4.2/ref/settings/#secure-proxy-ssl-header

# As per https://learn.microsoft.com/en-us/azure/app-service/configure-language-python#detect-https-session, 
# In Azure App Service, TLS/SSL termination happens at the network load balancers, 
# so all HTTPS requests reach your app as unencrypted HTTP requests. If your app 
# logic needs to check if the user requests are encrypted or not, inspect the X-Forwarded-Proto header.

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



# STATIC FILES
# -----------------------------------------------------------------------------

# See comments in base settings re: static files. The following are defined
# in base settings:
#  - STATIC_URL (the URL to use when referring to static files located in STATIC_ROOT)

# STATIC_ROOT is the absolute path to the directory where collectstatic() will 
# collect static files for deployment.
# See https://docs.djangoproject.com/en/4.1/ref/contrib/staticfiles/#collectstatic

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



# DATABASES
# -----------------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': os.environ['DBHOST'],
        'USER': os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASS'], 
        #'OPTIONS': {'sslmode': 'require'}
    }
}



# ADDITIONAL CEDAR SETTINGS
# -----------------------------------------------------------------------------

CRISPY_FAIL_SILENTLY = (os.getenv('CRISPY_FAIL_SILENTLY', default = 'False').lower() == 'true')


