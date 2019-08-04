from django.contrib import admin
from .models import User

# Register your models here.

admin.site.site_header = 'CSDN微课后台管理'
admin.site.index_title = '后台系统'
admin.site.site_title = '管理'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'account', 'username', 'money', 'gender', 'tel']
    list_filter = ['gender']
    search_fields = ['account', 'username']
