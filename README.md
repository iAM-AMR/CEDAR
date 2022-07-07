# CEDAR_web
 
Author: Charly Phillips (@phillipsclynn)


## Adapt to Azure

To setup CEDAR to be run on AZURE, we setup the repo based on https://github.com/Azure-Samples/djangoapp (azure-djangoapp).

Azure requires a requirements.txt file in the root directory. We generate this by running `pip freeze > requirements.txt` in our virtual environment. Two additional requirements are to use `whitenoise` and `psycopg2-binary` in place of psycopg2 (see https://github.com/Azure-Samples/djangoapp/issues/3). These were added manually to the requirements.txt file.


A new workflow was generated automatically from AZURE.


## Packages


#### Libraries for Auto-generated Documentation

You will need to download Sphinx, and Read the Docs Sphinx theme: `pipenv install -U sphinx sphinx-autobuild sphinx_rtd_theme`

In addition:
- `sphinxcontrib-django`

#### Miscellaneous Other Libraries

- `django-widget-tweaks`
- `django-extensions`
- `django-crispy-forms`

**Note**: Check that these are listed in the INSTALLED_APPS area of your Django site's `settings.py` file.