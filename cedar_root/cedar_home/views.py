

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    title = "Hello World"
    return render(request, 'cedar_home/base.html', {'title': title})