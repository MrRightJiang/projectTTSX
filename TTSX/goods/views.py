# coding=utf-8
from django.shortcuts import render,redirect
from models import *
from django.core.paginator import Paginator
from haystack.generic_views import SearchView

def index(request):
    good_list= []   #   替换index页面中的数据需要三个对象，最新和最热的商品信息，分类信息 ，依次实现并组合成数组[{}...{}]

    #  查询分类对象
    type_list = TypeInfo.objects.all()
    for t1 in type_list:
    # 1.查询出每个分类对象中最火的4个商品(点击量最多)
        clist=t1.goodsinfo_set.order_by('-gclick')[0:4]
    # 2.查询出每个分类对象中最新的4个商品
        nlist=t1.goodsinfo_set.order_by('-id')[0:4]

        good_list.append({'t1':t1,'clist':clist,'nlist':nlist})

    context={'title':'首页','show':1,'good_list':good_list}
    return render(request,'goods/index.html',context)

def goodlist(request,tid,pindex,orderby):       # 三个参数均为URL传的参数
    # 1.首页跳转至某一分类列表页， 列表页需要的该类型中的商品信息
    # 2. 展示固定显示每页图片个数，并分页
    # 使用get方法获取其中一个对象，当id不存在的时候会报错，则对异常处理

    # 接受url中的参数，查找对应的类型和所有商品
    t1=TypeInfo.objects.get(pk=int(tid))   #id=tid
        # 最新推荐的2件商品
    new_list = t1.goodsinfo_set.order_by('-id')[0:2]
        # 所有商品默认按id降序排列
    order_str='-id'
    desc = '1'
    # 现在做排序效果，（ 默认/价格[从大往小，从小往大]/人气 ）3种排序方式
    if orderby == '2':
        desc = request.GET.get('desc','1')  # 默认desc为1 ,并声明
        if desc == '1':
            order_str='gprice'
        else:
            order_str= '-gprice'
    elif orderby == '3':
        order_str='gclick'
    good_list=t1.goodsinfo_set.order_by(order_str)
    # 每页显示15条数据
    paginator=Paginator(good_list,10)
    # 获取当前页的数据
    page=paginator.page(pindex)
    # 防止人为填写页码，导致程序出错
    pindex1 = int(pindex)
    if pindex1 < 1:
        pindex1=1
    if pindex1 >paginator.num_pages:
        pindex1=paginator.num_pages

    # 即分页功能（‘首页 上一页 3 4 5/当前页 6 7 下一页 末页’）
    page_range = []
    if page.paginator.num_pages < 5:
        page_range = page.paginator.page_range  # 依次[1,2,3,4,5]
    elif page.number <= 2:  # 第1,2页
        page_range = range(1, 6)  # [1,2,3,4,5]
    elif page.number >= page.paginator.num_pages - 1:  # 倒数1,2页  [6,7,8,9,10]
        page_range = range(page.number - 4, page.paginator.num_pages + 1)
    else:  # 3,4,5,6,7
        page_range = range(page.number - 2, page.number + 3)

    context={'title':'商品列表页','t1':t1,'new_list':new_list,'page':page,'show':1,'orderby':orderby,
             'desc':desc,'page_range':page_range}
    return render(request,'goods/list.html',context)


def detail(request,id):
    try:
        # 获取商品对象
        g=GoodsInfo.objects.get(pk=id)
        # 新品推荐
        new_list = GoodsInfo.objects.order_by('-id')[0:2]
        # 人气量+=1
        g.gclick+=1
        g.save()

        context={'title':'商品详情页','show':1,'g':g,'new_list':new_list}
        response = render(request,'goods/detail.html',context)

        # 浏览记录功能 ，在个人用户中心显示5个浏览记录
        # 获取当前ID [1,2,3,4,5] =分割=> '1,2,3,4,5' 再拼接。   第一次查询没有值，则默认值为空
        gids = request.COOKIES.get('id_list','').split(',')
        print gids
        # 判断这个商品id是否存在,如果存在先删除，再插入到前面
        if id in gids:
            gids.remove(id)
        gids.insert(0,id)

        # 如果超过5个则删除最后一个
        if len(gids)>6:
            gids.pop()
        # 存入cookie,保存7天
        response.set_cookie('id_list',','.join(gids),max_age=60*60*24*7)
        return response
    except:
        return render(request,'404.html')

# 全文检索功能.完善模板中的图形画面则需要传递上下文，固在haystack中提供了一种重写get_context_data方法用于传递参数
class MySearchView(SearchView):

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        context['show']='1'      # 让模板继承base.html，传入参数（原有基础上新增键值）并显示出购物车
        page=context['page_obj']    # 获得context中独立封装了Page属性
        page_range = []             # 对搜索结果一个分页
        if page.paginator.num_pages < 5:
            page_range = page.paginator.page_range
        elif page.number <= 2:
            page_range = range(1, 6)
        elif page.number >= page.paginator.num_pages - 1:
            page_range = range(page.number - 4, page.paginator.num_pages + 1)
        else:  # 3,4,5,6,7
            page_range = range(page.number - 2, page.number + 3)
        context['page_range']=page_range
        return context

