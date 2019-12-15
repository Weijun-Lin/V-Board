from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'board'

urlpatterns = [
    path('', board, name="board"),
    path('set_board_info/', boardSet),
    path('get_info/<str:what>/', getInfo),
    path('set_list_name/', setListName),
    path('set_card_desc/', setCardDesc),
    path('add/<str:what>/', addListOrCard),
    path('set_card_name/', setCardName),
    path('upload_file/<int:bid>/<int:lid>/<int:cid>/<int:kind>/', uploadFile),
    path('upload_comment/', uploadComment),
]