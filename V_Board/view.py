from django.shortcuts import render

# Create your views here.
from django.http import *

def index(request: HttpRequest):
    return render(request, "index.html")
