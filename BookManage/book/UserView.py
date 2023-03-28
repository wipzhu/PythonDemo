from django.http import HttpResponse
from django.views import View


class UserView(View):

    def get(self, request):
        return HttpResponse('Get')

    def post(self, request):
        return HttpResponse('Post')

    def profile(self, request):
        return HttpResponse("Success")
