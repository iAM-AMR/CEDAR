
"""
Base Settings
"""

# A Django settings file contains the configuration of the Django installation.
# There are multiple CEDAR settings files - this is the BASE SETTINGS file.

# These settings are always used - both in deployment and in production.  
# This file is imported by settings_development.py and settings_production.py.

# The command pythonmanage.pydiffsettingsdisplays differences between the current 
# settings file and Django’s default settings.



from pathlib import Path

# All paths specified in the project are relative to BASE_DIR.
# Set BASE_DIR to the parent (.../cedar_root/) folder.
# The BASE_DIR is set relative to this file.
# This path is .../cedar_root/cedar_site/settings/settings_base, 
# Use parent x3 to traverse three levels from .../settings_base.

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# INSTALLED_APPS is a list of strings designating all applications that are 
# enabled in the Django installation. These applications are enabled by 
# default unless otherwise noted by comment.

INSTALLED_APPS = [
    # Add cedar_core (the true CEDAR app)
    'cedar_core.apps.CedarCoreConfig',
    # Django-autocomplete-light
    'dal',
    # Django-autocomplete-light
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Django-extensions
    'django_extensions',
    # Tweak the form field rendering in templates, not in python-level form
    # definitions.
    'widget_tweaks',
    # Build programmatic reusable layouts out of components, having full 
    # control of the rendered HTML without writing HTML in templates. 
    'crispy_forms',
    # Use Bootstrap5 in Django
    'django_bootstrap5',
    # Use Bootstrap5 with crispy_forms
    "crispy_bootstrap5",
    # Use WhiteNoise
    "whitenoise.runserver_nostatic",
]


# "Django middleware is a system that allows developers to hook into the 
# request-response cycle of a Django web application."

# Middleware specified in MIDDLEWARE are enabled; middlewear must also be 
# enabled in INSTALLED_APPS. Those specified below are enabled by default 
# unless otherwise noted. 

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Use Whitenoise
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# TEMPLATE is a list containing the settings for all template engines to be used 
# with Django. These are the default settings for TEMPLATE, which enable all 
# templates in the specified DIR (and all sub-directories).

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [BASE_DIR / 'cedar_site/templates'],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Password validation is configured in the AUTH_PASSWORD_VALIDATORS setting.
# These are the default validators.

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Enable Bootstrap 5. 
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
ROOT_URLCONF = 'cedar_site.urls'
WSGI_APPLICATION = 'cedar_site.wsgi.application'
LOGIN_URL = '/accounts/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True



# LOCALIZATION 
# -------------------------------------

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en','English'),
]

# TIME_ZONE is a string representing the time zone for this installation.

TIME_ZONE = 'America/Toronto'


# If USE_TZ is True, Django will use timezone-aware datetimes internally.
# In Django 5.0, the default value will change from False to True.
# https://docs.djangoproject.com/en/4.1/ref/settings/#use-tz

# Default = False
USE_TZ = True


# USE_I18N is a boolean that specifies whether Django’s translation system 
# should be enabled. This provides a way to turn it off, for performance.
# https://docs.djangoproject.com/en/4.1/ref/settings/#use-i18n

# Default = True
USE_I18N = True


# USE_L10N is a boolean that specifies if localized formatting of data will be enabled 
# by default or not. If this is set to True, Django will display numbers 
# and dates using the format of the current locale. The formatting system is 
# disabled by default. To enable, set USE_L10N = True. See: 
# https://docs.djangoproject.com/en/4.1/ref/settings/#use-l10n

# Default = True
USE_L10N = True



# STATIC FILES
# -------------------------------------

# Websites generally need to serve additional files such as images, JavaScript, 
# or CSS. In Django, we refer to these files as “static files”. Django provides 
# django.contrib.staticfiles to help you manage them. See 
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# There are more static parameters defined in the development and production
# environments.

# STATIC_URL is the URL to use when referring to static files located in 
# STATIC_ROOT. cedar.iam-amr.pub/static/path-within-STATIC_ROOT

STATIC_URL = 'static/'


# WhiteNoise comes with a storage backend which automatically takes care of 
# compressing your files and creating unique names for each version so they 
# can safely be cached forever.

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  


# This may be redundant.
STATICFILES_DIRS = [
    BASE_DIR / 'cedar_site/static'
]