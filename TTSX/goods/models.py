# coding=utf-8
from django.db import models
from tinymce.models import HTMLField

class TypeInfo(models.Model):
    ttitle=models.CharField(max_length=20)
    isDelete=models.BooleanField(default=False)
    # 在Admin后台中查看的类型时出现编码问题，所以使用str方法转义
    def __str__(self):
        return self.ttitle.encode('utf-8')

class GoodsInfo(models.Model):
    gtitle=models.CharField(max_length=50)
    gpic=models.ImageField(upload_to='goods')
    # 单价，总为位数为5位，小数位最多位2位
    gprice=models.DecimalField(max_digits=5,decimal_places=2)
    gclick=models.IntegerField(default=0)
    gunit=models.CharField(max_length=10)
    isDelete=models.BooleanField(default=False)
    # 详细页中的副标题
    subtitle=models.CharField(max_length=200)
    gkucun=models.IntegerField(default=100)
    # 详细页中的商品详情栏，用富文本编辑器
    gcontent=HTMLField()
    gtype=models.ForeignKey('TypeInfo')
