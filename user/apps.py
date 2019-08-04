from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'
    # 更改django管理的显示界面
    verbose_name = '用户管理'