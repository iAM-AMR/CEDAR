

# AZURE README



## Adapt to Azure

To setup CEDAR to be run on AZURE, we setup the repo based on https://github.com/Azure-Samples/djangoapp (azure-djangoapp).

Azure requires a requirements.txt file in the root directory. We generate this by running `pip freeze > requirements.txt` in our virtual environment. Two additional requirements are to use `whitenoise` and `psycopg2-binary` in place of psycopg2 (see https://github.com/Azure-Samples/djangoapp/issues/3). These were added manually to the requirements.txt file.


