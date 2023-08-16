"""cedar_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from . import views

#from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('favicon.ico', views.favicon),
    path('admin/', admin.site.urls),

    # Adding `accounts/` includes default authentication views as described:
    # https://docs.djangoproject.com/en/dev/topics/auth/default/#using-the-views
    # Login template must be provided (by default) at 'registration/login.html'.
    path('accounts/', include('django.contrib.auth.urls')),

    # Include CEDAR_CORE's 'urls.py'.
    path('', include('cedar_core.urls')),

]
