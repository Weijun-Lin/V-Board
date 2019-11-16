from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'login'

urlpatterns = [
    path('', login, name='login'),
]