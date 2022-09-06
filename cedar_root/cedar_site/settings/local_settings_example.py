

# Example of local_settings.py






import os


# Databases ---------------------------

# To use the default local database:

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

"""

# To connect to a postgres database:

""" 
DATABASES = { 
    'default': { 
        'ENGINE': 'django.db.backends.postgresql', 
        'NAME': 'db_name', 
        'USER': 'postgres', 
        'PASSWORD': 'password', 
        'HOST': 'ip-address or FQDN', 
        'PORT': '5432',
    } 
}
"""


# Graphviz ----------------------------

# To use Graphviz (https://graphviz.org/), replace <path_to> with the path to
# Graphviz on your system.

"""
os.environ["PATH"] += os.pathsep + '<path_to>/Graphviz/bin'
os.environ["PATH"] += os.pathsep + '<path_to>/Graphviz/lib'
os.environ["PATH"] += os.pathsep + '<path_to>/Graphviz/include'
"""


# PSQL --------------------------------

# To use PSQL, install Postgres and add /PostgreSQL/14/bin to the PATH.
# 'C:/Program Files/PostgreSQL/14/bin' is the Windows default installation location.

"""
os.environ["PATH"] += os.pathsep + 'C:/Program Files/PostgreSQL/14/bin'
"""


