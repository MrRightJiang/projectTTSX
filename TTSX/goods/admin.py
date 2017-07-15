# coding=utf-8
from django.contrib import admin
from models import *

# 后台中显示Type模型中的id和title属性
class TypeAdmin(admin.ModelAdmin):
    list_display = ['id','ttitle']

admin.site.register(TypeInfo,TypeAdmin)


# 显示商品的id，名字，价格，单位，库存
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id','gtitle','gprice','gunit','gkucun']
    list_per_page = 15  # 分页，每页最多15条信息

admin.site.register(GoodsInfo,GoodsAdmin)

