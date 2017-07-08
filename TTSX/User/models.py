from django.db import models

# Create your models here.

class UserInfo(models.Model):
    Uname=models.CharField(max_length=20)
    Upwd=models.CharField(max_length=40)
    Uphont=models.CharField(max_length=11)
    Umail=models.CharField(max_length=20)
    Ushou=models.CharField(default='',max_length=10)
    Uaddr=models.CharField(default='',max_length=100)
    Ucode=models.CharField(default='',max_length=6)


