from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
"""视图函数有两个要求：
1、第一个参数是接收请求
2、必须返回响应
"""


def index(request):
    context = {
        'title': '戳我去百度',
        'name': '马上双十一了，戳我有惊喜~'
    }
    return render(request, 'book/index.html', context)
    # return HttpResponse('Success')
