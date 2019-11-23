from django.shortcuts import render, redirect, reverse
from django.http import *
import models

def login(request: HttpRequest):
    # 如果已经登陆过直接跳转到用户主页面
    if request.session.get('is_login'):
        return redirect(reverse("home:home"))

    if request.method == "GET":
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        # login
        if request.POST.get('signin', -1) != -1:
            if models.Usr_Login.isLegal(email, password):
                request.session['is_login'] = True
                request.session['email'] = email
                return redirect(reverse("home:home"))
            else:
                return render(request, 'login.html', context={"login_error":True})
        # Register
        elif request.POST.get('signup', -1) != -1:
            usr_name = request.POST.get('name')
            if not models.Usr_Login.register(usr_name, email, password):
                return render(request, 'login.html', context={"reg_error":True})
            else:
                return render(request, 'login.html', context={"alert":True})

def logout(request):
    request.session.flush()
    return redirect(reverse('login:login'))