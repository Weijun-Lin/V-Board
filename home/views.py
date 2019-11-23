from django.shortcuts import render, redirect, reverse
from django.http import *
import models

def home(request:HttpRequest):
    if not request.session.get('is_login'):
	    return redirect(reverse('login:login'))
    person_boards = {"items":[{"name":"个人1", "starred": True}, {"name":"个人2", "starred": False}], "name":"个人看板", "icon":"user"}
    team1 = {"items":[{"name":"团队1", "starred": True}, {"name":"团队2", "starred": False}], "name":"团队1", "icon":"people"}
    team2 = {"items":[{"name":"团队1", "starred": True}, {"name":"团队2", "starred": False}], "name":"团队2", "icon":"people"}
    teams_boards = [team1, team2]
    user_name = "Joke-Lin"
    return render(request, 'home.html', context=locals())