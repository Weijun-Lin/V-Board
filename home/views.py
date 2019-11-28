from django.shortcuts import render, redirect, reverse
from django.http import *
from django.conf import settings
import os
import models


def home(request:HttpRequest):
    if not request.session.get('is_login'):
	    return redirect(reverse('login:login'))
    person_boards = {"items":[{"name":"个人1", "starred": True}, {"name":"个人2", "starred": False}], "name":"个人看板", "icon":"user"}
    team1 = {"items":[{"name":"团队1", "starred": True}, {"name":"团队2", "starred": False}], "name":"团队1", "icon":"people"}
    team2 = {"items":[{"name":"团队1", "starred": True}, {"name":"团队2", "starred": False}], "name":"团队2", "icon":"people"}
    teams_boards = [team1, team2]
    # 获取用户信息
    login_info = models.Usr_Login.getRecordByKey(request.session["email"])
    user_info = models.Usr_Info.getRecordByKey(request.session["uid"])
    # 获取用户名
    user_name = user_info[models.Usr_Info.name]
    # 获取头像
    avatar_path = models.Usr_Info.getRecordByKey(request.session["uid"])[models.Usr_Info.avatar]
    # 没有设置就为默认头像
    if len(avatar_path) == 0:
        avatar_path = "/media/avatar/default.jpg"
    # 获取用户个人介绍
    user_desc = user_info[models.Usr_Info.description]

    
    return render(request, 'home.html', context=locals(), )
        
        
