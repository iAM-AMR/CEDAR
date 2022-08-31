
import os

from django.http import HttpResponse,  FileResponse
from django.shortcuts import render


from django.views.decorators.http import require_GET

from django.conf import settings



def index(request):

    context = {'page_title': 'Welcome to CEDAR'}

    return render(request, 'cedar_site/index.html', context)


@require_GET
def favicon(request):
    file = open(os.path.join(settings.STATIC_ROOT, 'tree.svg'), "rb")
    return FileResponse(file)