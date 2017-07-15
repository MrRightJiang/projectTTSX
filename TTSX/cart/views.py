#coding=utf-8
from django.shortcuts import render,redirect
from models import *
from django.http import JsonResponse
from django.db.models import Sum
from User.zhuangshiqi import center_login
from User.models import UserInfo

def add(request):
    try:
        # 获取用户id
        user_id = request.session.get('uid')
        goods_id = int(request.GET.get('gid'))
        count = int(request.GET.get('count','1'))   #默认为1

        # 依次向数据库中添加数据
        # 1.当同一用户添加同一商品多个时。则count个数得递增
                # 直接向外键添加字段，需查看mysql表中的desc类型，外键会自动多加_id
        carts = CartInfo.objects.filter(user_id_id=user_id,goods_id_id=goods_id)
        print len(carts)
        if len(carts) == '1':
            print 3333
            c1 = carts[0]
            c1.count+=count
            c1.save()
        else:
                # 直接向外键添加字段，需查看mysql表中的desc类型，外键会自动多加_id
            c1 = CartInfo()
            c1.user_id_id=user_id
            c1.goods_id_id=goods_id
            c1.count=count
            c1.save()
        return JsonResponse({'isadd':1})
    except:
        return JsonResponse({'isadd':0})


def count(request):
    uid = request.session.get('uid')
    # 查询当前用户的数据库中的所有商品之和并返回                    聚合--count和          获取count和
    cart_count = CartInfo.objects.filter(user_id_id=uid).aggregate(Sum('count')).get('count__sum')
    print cart_count
    return JsonResponse({'cart_count':cart_count})

# 点击首页上的购物车,判断用户是否登陆
@center_login
def index(request):
    # 查询当前用户Id购物车对象
    uid = request.session.get('uid')
    ug_list = CartInfo.objects.filter(user_id_id=uid)
    context = {'title':'购物车','ug_list':ug_list,'show':1}
    return render(request,'cart/cart.html',context)

def delete(request):
    # 接受要删除的商品编号
    id = int(request.GET.get('id'))
    cart = CartInfo.objects.get(pk=id)
    cart.delete()
    return JsonResponse({'ok':1})

def edit(request):
    # 接受当前要修改的商品所在的购物车id
    id = int(request.GET.get('id'))
    count =int(request.GET.get('num'))
    cart = CartInfo.objects.get(pk=id)
    cart.count = count
    cart.save()
    return JsonResponse({'ok':1})

def order(request):
    uid = request.session.get('uid')
    user = UserInfo.objects.get(pk=uid)
    # 接受获取当前id的购物车对象
    print request.get_full_path()
    cart_list = request.POST.getlist('cartid')
    print cart_list
    carts = CartInfo.objects.filter(id__in=cart_list)
    context = {'title':'订单页面','order':'1','user':user,'carts':carts}
    return render(request,'cart/order.html',context)