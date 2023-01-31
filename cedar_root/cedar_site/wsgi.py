"""
WSGI config for cedar_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

Created V3.1 
"""


import os

from django.core.wsgi import get_wsgi_application

# If CEDAR_PRODUCTION is defined as an environment variable - regardless of its
# content - the app is running in production and should use production settings 
# in production_settings.py. Otherwise, the app is in development, and should 
# use the development settings in development_settings.py.

settings_module = "cedar_site.settings.production_settings" if 'CEDAR_PRODUCTION' in os.environ else 'cedar_site.settings.development_settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
