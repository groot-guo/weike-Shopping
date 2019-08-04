from django.utils.deprecation import MiddlewareMixin
from course import views as course_views
from django.shortcuts import reverse


class MyMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        """

        :param get_response:
        """
        super().__init__(get_response)
        # 初始化中间件
        print("init mymiddleware")

    def process_request(self, request):
        """

        :param request:
        :return:
        """
        # 方式一
        # request.context = {}
        # if 'session_user' in request.session.keys():
        #     session_user = request.context['session_user'] = request.session
        #     print(request.session['session_user']['account'])
        # if not session_user:
        #     if request.path.startswith('/video') or request.path.startswith('/user'):
        #         if request.path not in [reverse('user_login'), reverse('user_register')]:
        #             request.context['login_message'] = '请先登录'
        #             return course_views.index_handler(request)

        # 方式二
        request.context = dict(
            session_user=request.session['session_user'] if 'session_user' in request.session.keys() else None
        )
        if (not request.context['session_user']) \
                and (request.path.startswith('/video') or request.path.startswith('/user')) \
                and request.path not in [reverse('user_login'), reverse('user_register')]:
            request.context['login_message'] = '请先登录'
            return course_views.index_handler(request)

    def process_response(self, request, response):
        """

        :param request:
        :param response:
        :return:
        """
        # 必须return response
        print("process_response")
        return response
