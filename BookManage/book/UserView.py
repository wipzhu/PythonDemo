from django.http import HttpResponse
from django.views import View


class UserView(View):

    def get(self, request):
        return HttpResponse('Get')

    def post(self, request):
        return HttpResponse('Post')

    def put(self, request):
        return HttpResponse('Put')

    def profile(self, request):
        return HttpResponse("Success")

    def play(self):
        pass

    @classmethod
    def say(cls):
        pass

    @staticmethod
    def eat():
        pass
