"""
ASGI config for cedar_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

Created V3.1 
"""

import os

from django.core.asgi import get_asgi_application

settings_module = "cedar_site.settings.settings_default"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_asgi_application()
