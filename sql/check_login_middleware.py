from django.http import HttpResponseRedirect

class CheckLoginMiddleware(object):
    def process_request(self, request):
        """
        本系统没有采用django.contrib.auth组件, 自己简单实现了一把认证系统
        该函数在每个函数之前检查是否登录, 若未登录, 则重定向到/login/
        """
        if request.session.get('login_username', False) in (False, '匿名用户'):
            # http://127.0.0.1:8000/200/?type=20
            # request.get_full_path()返回的是 /200/?type=20 (获取当前url, 包含参数)
            # request.path返回的是 /200 (获取当前url, 不包含参数)
            if request.path not in ('/login/', '/authenticate/'):
                return HttpResponseRedirect('/login/')