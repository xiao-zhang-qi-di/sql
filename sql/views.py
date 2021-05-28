import json

from django import http
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .models import users


def login(request):
    return render(request, 'login.html')

# ajax接口, 登录页面调用, 用来验证用户名密码
# 取消csrf—token验证
@csrf_exempt
def authenticate(request):
    """认证机制做的非常简单, 密码没有加密, 建议类似md5单项加密即可"""
    # 判断当前是否为 AJAX 请求
    if request.is_ajax():
        strUsername = request.POST.get('username')
        strPassword = request.POST.get('password')
    else:
        strUsername = request.POST['username']
        strPassword = request.POST['password']
    # 服务端二次验证参数
    result = {}
    if strUsername == "" or strPassword == "" or strUsername is None or strPassword is None:
        result = {
            "status": 2,
            "msg": "登录用户名或密码为空, 请重新输入！",
            "data": ""
        }
        return http.HttpResponse(json.dumps(result), content_type="application/json")

    login_user = users.objects.filter(username=strUsername, password=strPassword)
    if len(login_user) == 1:
        result = {
            "status": 0,
            "msg": "ok",
            "data": ""
        }
    else:
        result = {
            "status": 1,
            "msg": "用户名或密码错误，请重新输入！",
            "data": ""
        }
    return http.HttpResponse(json.dumps(result), content_type="application/json")

def allworkflow(request):
    context = {'currentMenu': "allworkflow"}
    return render(request, 'allWorkflow.html', context)

def submitSql(request):
    context = {'currentMenu': 'submitsql'}
    return render(request, 'submitSql.html', context)