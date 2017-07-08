# coding=utf-8
from django.shortcuts import render,redirect
from hashlib import sha1
from models import *
from django.http import JsonResponse,HttpResponse
import datetime
from zhuangshiqi import *
# Create your views here.

def register(request):
    context={'title':'注册','top':'0'}
    return render(request,'User/register.html',context)

def register_headle(request):

    # 接受数据
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('user_pwd')
    umail=post.get('user_email')
    # 加密密码
    s1=sha1()
    s1.update(upwd)
    upwd_sha1=s1.hexdigest()
    #  创建对象，保存到数据库
    user=UserInfo()
    user.Uname=uname
    user.Upwd=upwd_sha1
    user.Umail=umail
    user.save()
    # 完成跳转登陆页
    return redirect('/user/login/')

def register_valid(request):
    # 注册名称是是否存在
    uname=request.GET.get('uname')
    result=UserInfo.objects.filter(uname=uname).count()
    context={'result':result}
    return JsonResponse(context)

def login(request):
    uname = request.COOKIES.get('uname','')     # 当用户点击了记住用户名，先登陆处理中存入cookie，再次登陆时取出，显示
    context={'title':'登陆','top':'0','uname':uname}
    return render(request,'User/login.html',context)

def login_headle(request):
    # 获取数据与数据库中进行比较验证
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('user_pwd')
    uname_jz = post.get('uname_jz','0') # 获取是否勾选了 ‘记住用户名’的值，默认为1，如没有勾选则默认为0

    # 数据库中为加密后的密码，所以将获取的密码进行加密比较
    s1=sha1()
    s1.update(upwd)
    upwd_sha1=s1.hexdigest()

    # 无论是执行哪段程序，都将Uname返回，切呈现在用户名的那一栏中
    context={'title':'登陆','uname':uname,'upwd':upwd,'top':'0'}
    # 根据用户名查询数据，未查到返回是【】，查询到了则返回的是[userinfo]对象
    user=UserInfo.objects.filter(Uname=uname)
    if len(user)==0:    # 用户名错误
        context['name_error']='1'
        return render(request,'User/login.html',context)
    else:
        # 用户名正确，现在比对密码
        if user[0].Upwd == upwd_sha1:   # 密码正确，登陆成功
            # return redirect('/user/') , 登陆成功，应直接跳转用户中心页面，但还有功能未完善，不能直接return
            # 1.记录当前的用户登陆状态（session），完成个人中心提取信息功能
            request.session['uid'] = user[0].id
            request.session['uname'] = uname    #登陆成功后。置顶菜单栏显示用户名称
            # 2. 记住用户名
            path=request.session.get('url_path','/')    #中间件获取的地址

            response=redirect(path)         # 1.赋值，redirect是HttpResponse的子类，继承了父类set_cookie方法
                                            # 2.在哪登陆，登陆成功后就跳回哪个地方（中间件）

            if uname_jz == '1':
                                #   键   ， 值（不写默认为空） ，   过期时间：当前时间+ 未来7天
                response.set_cookie('uname',uname,expires=datetime.datetime.now()+datetime.timedelta(days=7))

            else:
                                        #       过期秒数，设未来值，-1马上过期
                response.set_cookie('uname','',max_age=-1)

            return response

        else:
            # 密码错误,得通知html模块中显示，固在context中新增一个属性
            context['pwd_error'] = '1'
            return render(request,'User/login.html',context)

def loginout(request):  # 退出功能试图，清空session的缓存，直接跳转登陆页
    request.session.flush()
    return redirect('/user/login/')

@center_login
def center(request):
    user=UserInfo.objects.get(pk=request.session['uid'])
    context={'title':'个人中心','user':user}
    return render(request,'User/center.html',context)

@center_login
def order(request):
    context = {'title':'用户订单'}
    return render(request,'User/order.html',context)

@center_login
def site(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    if request.method=='POST':
        post=request.POST
        user.Ushou=post.get('ushou')
        user.Uaddr=post.get('uaddr')
        user.Ucode=post.get('ucode')
        user.Uphont=post.get('uphone')
        user.save()
    context = {'title':'收货地址','user':user}
    return render(request,'User/site.html',context)

'''
在页面A中，转到登录页，登录完成后，转回A页
****=request.path

第一个问题：如果这段代码写在视图中，则需要维护的视图非常多
第二个问题：对于必须登录的页面，由于装饰器的影响，在未登录时，并不会执行
问题一的解决：让可以在每个视图中执行
问题二的解决：设立中间件middleware（可以干预程序的运行顺序），在视图执行之前记录路劲

用户模块写完
'''


