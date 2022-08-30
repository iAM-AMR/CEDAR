

from django.http import HttpResponse,  FileResponse
from django.shortcuts import render


from django.views.decorators.http import require_GET

from django.conf import settings



def index(request):
    return render(request, 'cedar_site/index.html')


@require_GET
def favicon(request):
    file = (settings.BASE_DIR / "cedar_site" / "static" / "tree.svg").open("rb")
    return FileResponse(file)