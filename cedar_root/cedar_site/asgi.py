"""
ASGI config for cedar_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

Created V3.1 
"""


import os

from django.core.asgi import get_asgi_application

# If WEBSITE_HOSTNAME is defined as an environment variable, we're running
# in production on Azure App Service, and should use the production settings in 
# production_settings.py. Otherwise, we're running in development, and should 
# use the development settings is development_settings.py.

settings_module = "cedar_site.settings_production" if 'WEBSITE_HOSTNAME' in os.environ else 'cedar_site.settings_stage'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_asgi_application()
