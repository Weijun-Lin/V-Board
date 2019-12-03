from django.shortcuts import render, redirect, reverse
from django.http import *
from django.conf import settings
import os
import models

# Create your views here.

def board(request:HttpRequest):
    # 没登陆直接访问 跳转到登陆界面
    if not request.session.get('is_login'):
	    return redirect(reverse('login:login'))

    if request.method == "GET":
        # 错误格式 直接返回到首页
        if request.GET.get("id") == None or request.GET.get("kind") == None:
            return redirect(reverse('home:home'))

        # 获取数据
        uid = request.session["uid"]
        bid = int(request.GET.get("id"))
        kind = int(request.GET.get("kind"))
        # 没有则返回到主界面
        
        # 在导航栏添加新建列表
        navbar_add_list = True

        # 获取相应信息
        board_type = models.Person_Board if kind == 0 else models.Team_Board
        list_type = models.P_List if kind == 0 else models.T_List
        card_type = models.P_Card if kind == 0 else models.T_Card
        # 看板信息
        board_info = models.Board.getBoardByBid(board_type, bid)[0]
        lids = models.List.getListsByBid(list_type, bid)  # lid信息
        # 列表信息
        lists = []
        for lid_dict in lids:
            lid = lid_dict[models.List.lid]
            cards = models.Card.getCardsByLid(card_type, lid) # 字典的列表
            lists.append({"info":lid_dict, "cards": cards}) # 包含 lid, name 以及 lid 对应的card

        # 以下信息同 home.view 构建导航栏所需要的信息
        # 获取用户信息
        login_info = models.User_Login.getRecordByKey(request.session["email"])
        user_info = models.User_Info.getRecordByKey(uid)

        # 获取用户名
        user_name = user_info[models.User_Info.name]

        # 获取头像
        avatar_path = models.User_Info.getRecordByKey(uid)[models.User_Info.avatar]
        # 没有设置就为默认头像
        if len(avatar_path) == 0:
            avatar_path = "/media/avatar/default.jpg"

        # 获取用户个人介绍
        user_desc = user_info[models.User_Info.description]
        
        return render(request, "board.html", context=locals())