from django.utils.deprecation import MiddlewareMixin


class testMiddlewareMixin(MiddlewareMixin):

    def __int__(self):
        super().__init__()

    def process_request(self, request):
        print("每次处理请求前都会调用")
        username = request.COOKIES.get('username')
        if username:
            print("有用户信息")
        else:
            print("没有用户信息")

    def process_response(self, request, response):
        print("每次响应前都会调用")
        return response
