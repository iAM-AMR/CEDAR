

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    title = "Hello World"
    page_title = "CEDAR"
    return render(request, 'cedar_home/index.html', {'title': title, 'page_title': page_title})

    """ 
    Working w. vars

    def index(request):
    title = "Hello World"
    page_title = "CEDAR"
    return render(request, 'cedar_home/index.html', {'title': title, 'page_title': page_title}) 
    """