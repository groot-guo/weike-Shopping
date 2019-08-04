from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import User
from course import views as course_views
from course.models import Course


# Create your views here.
def index_handler(request):
    """
    用户首页的显示
    :param request:
    :return:返回用户首页
    """
    context = request.context
    session_user = request.session['session_user']
    user = User.objects.get(id=session_user.get('id'))
    context['user'] = user
    if request.method == 'GET':
        return render(request, 'user.html', context)
    else:
        user.username = request.POST.get('username')
        user.gender = request.POST.get('gender')
        user.tel = request.POST.get('tel')
        user.save()
        return redirect(reverse('user_index'))


def course_handler(request):
    """
    用户课程的显示
    :param request:
    :return:用户的课程界面
    """
    context = request.context
    session_user = request.session['session_user']
    course_s = User.objects.get(id=session_user.get('id')).userBuyer_set.all()
    context['course_s'] = course_s
    return render(request, 'user_course.html', context)


def shoppingCart_handler(request):
    """
    用户的购物车界面
    :param request:
    :return:用户购物车界面
    """
    context = request.context
    session_user = request.session['session_user']
    course_s = User.objects.get(id=session_user.get('id')).userShoppingcart_set.all()
    context['course_s'] = course_s
    return render(request, 'user_shoppingcart.html', context)


def login_handler(request):
    """
    登录界面
    :param request:
    :return:课程首页
    """
    if request.method != 'POST':
        return HttpResponse(status=403)
    context = request.context
    account = request.POST.get('account')
    password = request.POST.get('password')
    user_s = User.objects.filter(account=account, password=password)
    if user_s:
        user = user_s[0]
        request.session['session_user'] = {'id': user.id, 'account': user.account}
        # context['session_user'] =
        print(request.session['session_user']['account'])
        return redirect(reverse('course_index'))
    else:
        context['login_message'] = '账号密码错误'
    return course_views.index_handler(request)


def register_handler(request):
    """
    注册界面
    :param request:
    :return:课程首页
    """
    context = request.context
    if request.method != 'POST':
        return HttpResponse(status=403)
    account = request.POST.get('account')
    password = request.POST.get('password')
    try:
        user_exists = User.objects.filter(account=account).exists()
        if not user_exists:
            user = User(account=account, password=password)
            user.save()
            request.session['session_user'] = {'id': user.id, 'account': user.account}
        else:
            context['register_message'] = '账号已存在'
    except:
        context['register_message'] = '服务器异常'
    finally:
        return course_views.index_handler(request)


def logout_handler(request):
    """
    注销
    :param request:
    :return:课程首页
    """
    request.session['session_user'] = None
    request.session.clear()
    return redirect(reverse('course_index'))


def purchase_handler(request, course_id):
    """
    购买流程
    :param request:
    :param course_id:课程Id
    :return:购物车成功与失败的信息
    """
    context = request.context
    try:
        course = Course.objects.get(id=course_id)
        session_user = request.session['session_user']
        user = User.objects.get(id=session_user.get('id'))
        if user.money >= course.price:
            user.userBuyer_set.add(course)
            user.money -= course.price
            user.save()
            context['message'] = '购买成功'
        else:
            context['message'] = '余额不足'
    except:
        context['message'] = '购买失败'
    finally:
        return render(request, 'user_message.html', context)


def addShoppingCart_hanlder(request, course_id):
    """
    添加购物车
    :param request:
    :param course_id:课程Id
    :return:返回购物车信息显示
    """
    context = request.context
    try:
        course = Course.objects.get(id=course_id)
        session_user = request.session['session_user']
        user = User.objects.get(id=session_user.get('id'))
        user.userShoppingcart_set.add(course)
        user.save()
        context['message'] = '添加购物车成功'
    except:
        context['message'] = '添加购物失败'
    return render(request, 'user_message.html', context)
