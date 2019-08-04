from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index_handler, name='user_index'),
    path('course', views.course_handler, name='user_course'),
    path('shoppingCart', views.shoppingCart_handler, name='user_shoppingCart'),
    path('login', views.login_handler, name='user_login'),
    path('register', views.register_handler, name='user_register'),
    path('logout', views.logout_handler, name='user_logout'),
    re_path('purchase/(.+)', views.purchase_handler, name='user_purchase'),
    re_path('addShoppingCart/(.+)', views.addShoppingCart_hanlder, name='user_addShoppingCart'),
]
