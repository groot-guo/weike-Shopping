from django.db import models


# Create your models here.
class User(models.Model):
    GENDER_CHOICES = (
        (0, '男'),
        (1, '女')
    )

    class Meta():
        verbose_name = verbose_name_plural = '用户表'

    id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=32, unique=True, verbose_name='账号')
    password = models.CharField(max_length=32, verbose_name='密码')
    username = models.CharField(max_length=32, verbose_name='用户名', default='')
    money = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='余额', default=0)
    gender = models.PositiveSmallIntegerField(default=0, verbose_name='性别', choices=GENDER_CHOICES)
    tel = models.CharField(max_length=11, default='', verbose_name='手机号')

    def __str__(self):
        return self.account
