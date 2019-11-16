from django.shortcuts import render
import models   # 导入数据库表

# Create your views here.
from django.http import *

def index(request: HttpRequest):
    return render(request, "index.html")
