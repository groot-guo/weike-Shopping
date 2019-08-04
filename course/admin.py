from django.contrib import admin
from .models import Course, Category


# Register your models here.



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'courseName', 'pCategory', 'price', 'summary', 'status', 'createDatetime']
    # 增加显示效果，右边是被选中的
    filter_horizontal = ['userBuyer', 'userShoppingcart']
    list_filter = ['status', 'createDatetime']
    search_fields = ['courseName', 'price']
