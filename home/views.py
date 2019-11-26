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
    user_name = "Joke-Lin"
    avatar_path = models.Usr_Info.getRecordByKey(request.session["uid"])[models.Usr_Info.avatar]
    if len(avatar_path) == 0:
        avatar_path = "/media/avatar/default.jpg"
    return render(request, 'home.html', context=locals(), )


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
        models.Usr_Info.update(request.session["uid"], "Joke-Lin", avatar_path ,"")
        return HttpResponse(avatar_path)
        
        
