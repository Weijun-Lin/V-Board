from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'board'

urlpatterns = [
    path('', board, name="board"),
    path('set_board_info/', boardSet),
    path('get_board_info/', getBoardInfo),
]