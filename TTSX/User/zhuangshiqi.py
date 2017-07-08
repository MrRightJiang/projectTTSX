# coding=utf-8
from django.shortcuts import redirect

def center_login(func):
    # 装饰器，针对用户点击用户中心时，得跳转登陆页
    def func1(request):
        #查询request.session中是否有uID来进行判定是否有登陆
        #如没有UID则说明没有登陆，跳转登陆页

        if request.session.has_key('uid'):
            return func(request)
        else:
            return redirect('/user/login/')

    return func1

