from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index_handler, name='course_index'),
    re_path('course/(.+)', views.course_handler, name='course_course'),
    re_path('video/(.+)', views.video_handler, name='course_video'),
    re_path('videoStream/(.+)', views.videoStream_handler, name='course_videoStream')
]
