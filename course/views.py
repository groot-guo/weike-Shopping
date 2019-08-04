from django.shortcuts import render, reverse, redirect, HttpResponse
from .models import Course, Category
from user.models import User
from django.http import StreamingHttpResponse
import os


# Create your views here.
def index_handler(request):
    """
    课程主页
    :param request:
    :return:课程首页信息的展示
    """
    context = request.context
    course_data_s = []
    category_s = Category.objects.all()
    for category in category_s:
        course_data_s.append(
            {
                'category': category.name,
                'course_s': category.courses_set.all()
            }
        )
    context['course_data_s'] = course_data_s
    print(context)
    return render(request, 'index.html', context)


def course_handler(request, course_id):
    """
    显示课程信息
    :param request:
    :param course_id:课程Id
    :return:课程的主页
    """
    context = request.context
    try:
        course = Course.objects.get(id=course_id)
        session_user = request.session.get('session_user', None)
        if session_user:
            context['view_perssion'] = User.objects.filter(id=session_user.get('id'),
                                                           userBuyer_set__id=course.id).exists()
        context['course'] = course
        return render(request, 'course.html', context)
    except:
        return HttpResponse(status=404)


def video_handler(request, course_id):
    """
    视频界面显示
    :param request:
    :param course_id:课程Id
    :return:视频界面显示 or 课程主页
    """
    context = request.context
    try:
        course = Course.objects.get(id=course_id)
        session_user = request.session['session_user']
        boolean_buyed = User.objects.filter(id=session_user.get('id'), userBuyer_set__id=course_id).exists()
        if boolean_buyed:
            context['course'] = course
            return render(request, 'video.html', context)
        else:
            return redirect(reverse('course_course'), args=(course.id,))
    except:
        return HttpResponse(status=404)


def videoStream_handler(request, course_id):
    """
    读取视频显示
    :param request:
    :param course_id:课程Id
    :return:视频读取，or 未购买返回购买信息
    """
    def read_video(path):
        """

        :param path:
        :return:
        """
        with open(path, 'rb') as f:
            while True:
                data = f.read(1024 * 10)
                if data:
                    yield data
                else:
                    break

    context = request.context
    try:
        course = Course.objects.get(id=course_id)
        session_user = request.session['session_user']
        boolean_buyed = User.objects.filter(id=session_user.get('id'), userBuyer_set__id=course_id).exists()
        if boolean_buyed:
            context['course'] = course
            response = StreamingHttpResponse(read_video(course.fileName.__str__()), status=206)
            response['Content-Range'] = 'bytes 0-10240/%s' % os.path.getsize(course.fileName.__str__())
            return response
        else:
            return redirect(reverse('course_course'), args=(course.id,))
    except:
        return HttpResponse(status=404)


