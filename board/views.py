from django.shortcuts import render, redirect, reverse
from django.http import *
from django.conf import settings
import os
import json
import models

# Create your views here.

def isOwner(_bid, _uid, _board_type):
    owner_id = models.Board.getBoardByBid(_board_type, _bid)[0][_board_type.owner_id]
    if _board_type == models.Person_Board:
        return _uid == owner_id
    else:
        return _uid == models.Team.getRecordsByTid(owner_id)[0][models.Team.uid]

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

        # 判断是否为 owner
        isowner = isOwner(bid, uid, board_type)
        # if kind == 0 and owner_id == 
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


def boardSet(request:HttpRequest):
    if request.method == "POST":
        # 获取数据
        data = json.loads(request.body)
        print(data)
        uid = request.session["uid"]
        bid = int(data["bid"])
        kind = int(data["kind"])

        # 获取相应信息
        board_type = models.Person_Board if kind == 0 else models.Team_Board
        list_type = models.P_List if kind == 0 else models.T_List
        card_type = models.P_Card if kind == 0 else models.T_Card

        
        board_name = data["board_name"]
        desc = data["desc"]
        # 状态码 status: 0 success ; 1 empty title; 2 illegal title; 3 too long
        reponse = {}    # 返回的字典
        status = 0
        if board_name == "":
            status = 1
        elif len(board_name) > 50:
            status = 3
        else:
            # 判断是否重复
            owner_id = models.Board.getBoardByBid(board_type, bid)[0][board_type.owner_id]
            boards = models.Board.getBoardsByOwner(board_type, owner_id)
            for board in boards:
                if board[board_type.owner_id] != owner_id and board[board_type.name] == board_name:
                    status = 2
                    break
            if status != 2:
                models.Board.setInfo(board_type, bid, board_name, desc)

        reponse['status'] = status
        return JsonResponse(reponse)

def getBoardInfo(request:HttpRequest):
    if request.method == "GET":
        bid = int(request.GET.get("id"))
        kind = int(request.GET.get("kind"))
        board_type = models.Person_Board if kind == 0 else models.Team_Board
        return JsonResponse(models.Board.getBoardByBid(board_type, bid)[0])