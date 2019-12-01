from django.shortcuts import render, redirect, reverse
from django.http import *
from django.conf import settings
import os
import models


def home(request:HttpRequest):
    # 没登陆直接访问 跳转到登陆界面
    if not request.session.get('is_login'):
	    return redirect(reverse('login:login'))

    uid = request.session["uid"]
    # 传递给模板的格式 board:{"items":[{"name":"个人1", "starred": True}], "name":"个人看板", "icon":"user"}

    # 获取个人看板
    person_boards = {"name":"个人看板", "icon":"user", "items":[], "type":0}
    p_board_records = models.Board.getBoardsByOwner(models.Person_Board, uid)
    for item in p_board_records:
        person_boards["items"].append(item)

    # 获取团队看板
    teams_boards = []
    tids = models.Team_Member.getTeams(uid)
    print(tids)
    # 对每一个团队
    for tid_dict in tids:
        tid = tid_dict[models.Team_Member.tid]
        team_name = models.Team.getRecordsByTid(tid)[0][models.Team.name] # 获取团队名字
        uids = models.Team_Member.getTeammates(tid)  # 获取uid
        # 获取成员的Email列表
        teammates = []
        for i in uids:
            team_info = {}
            team_info["email"] = (models.User_Login.getEmailByUid(i[models.User_Login.uid])[0][models.User_Login.email])
            team_info["uid"] = i[models.User_Login.uid]
            team_info["owner_id"] = models.Team.getRecordsByTid(tid)[0][models.Team.uid]
            teammates.append(team_info)

        team = {"name":team_name, "tid":tid, "icon":"people", "items":[], "TID":tid, "teammates":teammates, "type":1}
        t_board_records = models.Board.getBoardsByOwner(models.Team_Board, tid)
        # 获取该团队看板
        for item in t_board_records:
            team["items"].append(item)
        teams_boards.append(team)
    print(teams_boards)

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
    
    return render(request, 'home.html', context=locals())