from django.db import models

class CartInfo(models.Model):
    user_id = models.ForeignKey('User.UserInfo')
    goods_id = models.ForeignKey('goods.GoodsInfo')
    count = models.IntegerField()