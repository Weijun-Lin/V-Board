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
        print("body:")
        print(request.body)
        print("data:")
        print(data)
        print(request.POST.items())
        return HttpResponse("OK")


def userSet(request:HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body)     
        print(data)
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
        elif login_info[models.Usr_Login.password] != srcpass:
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
        print(data)
        return JsonResponse(data)


def getUsrInfo(request:HttpRequest):
    user_info = models.User_Info.getRecordByKey(request.session["uid"])
    return JsonResponse(user_info)