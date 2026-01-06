"""
WSGI config for cedar_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

Created V3.1 
"""


import os

from django.core.wsgi import get_wsgi_application

settings_module = "cedar_site.settings.settings_default"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
