from django.shortcuts import render
import models   # 导入数据库表
import os
import json
from django.conf import settings


# Create your views here.
from django.http import *


def index(request:HttpRequest):
    return render(request, "index.html")


def setAvatar(request:HttpRequest):
    if request.method == "POST":
        avatar = request.FILES.get("avatar", None)
        if not avatar:
            return HttpResponse("error")

        avatar_path = open(os.path.join(settings.BASE_DIR, 'media', 'avatar', request.session['email']+".jpg"), "wb+")
        for chunk in avatar.chunks():      # 分块写入文件
            avatar_path.write(chunk)
        avatar_path.close()

        avatar_path = "/media/avatar/{}.jpg".format(request.session['email'])
        models.User_Info.update(request.session["uid"], "Joke-Lin", avatar_path ,"")
        return HttpResponse(avatar_path)


def addBoard(request:HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body)
        response = {}
        # 状态码 status: 0 success ; 1 empty title; 2 illegal title; 3 too long
        status = 0
        name = data["title"]
        kind = int(data["type"])
        is_public = data["ispublic"]

        if name == "":
            status = 1
        elif len(name) > 80:
            status = 3
        else:
            # 向个人或者团队中插入数据
            board_kind = models.Person_Board if kind == 0 else models.Team_Board
            ownerid = request.session["uid"] if kind == 0 else kind
            boards = models.Board.getBoardsByOwner(board_kind, ownerid)
            for board in boards:
                if board[board_kind.name] == name:
                    status = 2
                    break
            if status != 2:
                models.Board.insert(board_kind, name, '', ownerid, is_public)
                print(models.Board.getLastByBid(board_kind))
                response = {**response, **models.Board.getLastByBid(board_kind)}
                response["type"] = kind

        response["status"] = status
        return JsonResponse(response)


def userSet(request:HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body)
        reponse = {}    # 返回的字典
        # 获取记录
        login_info = models.User_Login.getRecordByKey(request.session["email"])
        user_info = models.User_Info.getRecordByKey(request.session["uid"])
        # 修改昵称 以及 描述
        reponse['nickname'] = data['nickname']
        # 如果不为空 则更新 用户名以及自我描述
        if data['nickname'] != '':
            models.User_Info.update(request.session["uid"], data['nickname'], user_info[models.User_Info.avatar], data["desc"])
        # 修改密码
        # 状态码 status: 0 success ; 1 wrong password; 2 illegal new password; 3 unequal;4 not modify password
        status = 0
        srcpass, newpass, repass = data["srcpass"], data["newpass"], data["repass"]
        if newpass == '' or repass == '':
            status = 2
        elif newpass != repass:
            status = 3
        elif login_info[models.User_Login.password] != srcpass:
            status = 1
        else:
            models.User_Login.changePassword(request.session["email"], newpass)
        if newpass == '' and srcpass == '' and repass == '':
            status = 4
        reponse['status'] = status

        return JsonResponse(reponse)


def addTeam(request:HttpRequest):
    if request.method == 'POST':
        data = json.loads(request.body)
        # 状态码 status: 0 success ; 1 empty title; 2 illegal title; 3 duplicate member;4 exist illegal member;5 too long
        status = 0
        response = {}
        name = data["name"]
        desc = data["desc"]
        print(data)
        # 判断团队标题是否已经创建过
        if name == '':
            status = 1
        elif len(name) > 80:
            status = 5
        elif not models.Team.isLegalName(request.session["uid"], name):
            status = 2
        else:
            # 判断成员是否合法
            members = data["member"]
            members.append(request.session["email"])
            # 重复成员
            if len(members) != len(set(members)):
                print(members)
                print(set(members))
                status = 3
            else:
                uids = []
                for member in data["member"]:
                    uid = models.User_Login.getUidByEmail(member)
                    # 不存在的成员
                    if uid == 0:
                        status = 4
                        response["illegal_email"] = member
                        break
                    uids.append(uid)
                if status == 0:
                    models.Team.createTeam(request.session["uid"], name, uids)
        
        response["status"] = status
        return JsonResponse(response)


def getUsrInfo(request:HttpRequest):
    user_info = models.User_Info.getRecordByKey(request.session["uid"])
    return JsonResponse(user_info)

def try_board(request:HttpRequest):
    kind = int(request.GET.get("kind"))
    board_kind = models.Person_Board if kind == 0 else models.Team_Board
    bid = request.GET.get("id")
    name = models.Board.getBoardByBid(board_kind, bid)
    return HttpResponse("<h1>进入看板 {} </h1>".format(name))


def delete(request:HttpRequest, what:str):
    if not request.session["is_login"]:
        return HttpResponse('')
    # 删除看板 通过bid
    if what == "board":
        kind = int(request.GET.get("kind"))
        board_kind = models.Person_Board if kind == 0 else models.Team_Board
        bid = int(request.GET.get("id"))
        models.Board.deleteByBid(board_kind, bid)
    # 删除团队 通过tid
    elif what == "team":
        tid = int(request.GET.get("id"))
        models.Team.deleteByTid(tid)
    elif what == "teammate":
        uid = int(request.GET.get("uid"))
        tid = int(request.GET.get("tid"))
        models.Team_Member.deleteMember(tid, uid)
    elif what == "list":
        kind = int(request.GET.get("kind"))
        lid = int(request.GET.get("id"))
        list_type = models.P_List if kind == 0 else models.T_List
        models.List.deleteByLid(list_type, lid)
    elif what == "card":
        kind = int(request.GET.get("kind"))
        cid = int(request.GET.get("id"))
        card_type = card_type = models.P_Card if kind == 0 else models.T_Card
        models.Card.deleteByCid(card_type, cid)

    return HttpResponse('')


def invite(request:HttpRequest):
    response = {}
    # 状态码 status: 0 success ; 1 empty email; 2 existed; 3 not existed;
    status = 0
    email = request.GET.get("email")
    tid = int(request.GET.get("tid"))
    if email == "":
        status = 1
    else:
        uid = models.User_Login.getUidByEmail(email)
        if uid == 0:
            status = 3
        else:
            records =  models.Team_Member.getTeammates(tid)
            for record in records:
                if uid == record[models.Team_Member.uid]:
                    status = 2
                    break
            if status != 2:
                models.Team_Member.insert(tid, uid)

    response["status"] = status
    response["email"] = email
    return JsonResponse(response)