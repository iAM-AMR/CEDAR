

# BASE SETTINGS

# This file sets base settings, shared between development and production
# environments.



from pathlib import Path

# Get to the parent /cedar_root/ folder.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# INSTALLED_APPS are default unless otherwise specified.
INSTALLED_APPS = [
    # cedar_core (the CEDAR app)
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
    # Use Font Awesome
    #'fontawesomefree',
    # Use WhiteNoise
    "whitenoise.runserver_nostatic",
]



# MIDDLEWARE are default unless otherwise specified.
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


# https://docs.djangoproject.com/en/4.1/ref/settings/#templates

# Here’s a setup that tells the Django template engine to load templates from the templates subdirectory inside each installed application:

# Here, we specify Templates to collect templates out of a common directory. 

# - 'APP_DIRS':
#   Default: False
#   Whether the engine should look for template source files inside installed applications.
#
# - 
# https://docs.djangoproject.com/en/4.1/ref/templates/api/#using-requestcontext

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



# Use all available password validators. See:
# https://docs.djangoproject.com/en/4.1/topics/auth/passwords/#enabling-password-validation

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



CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
ROOT_URLCONF = 'cedar_site.urls'
WSGI_APPLICATION = 'cedar_site.wsgi.application'
LOGIN_URL = '/accounts/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True



# LOCALIZATION 
# -----------------------------========

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