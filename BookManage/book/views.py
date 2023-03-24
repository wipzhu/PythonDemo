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

# from book.models import BookInfo
#
#################新增数据#################
# book = BookInfo(
#     name='Django', author='wipzhu', pub_date='2023-03-24',
#     price=12.8, read_count=10, comment_count=20, is_delete=0
# )
# book.save()
# BookInfo.objects.create(
#     name='测试开发', author='wipzhu', pub_date='2023-03-24',
#     price=12.8, read_count=10, comment_count=20, is_delete=0
# )
#################修改数据#################
# book = BookInfo.objects.get(id=6)
# book.name = '运维开发入门'
# book.save()
# BookInfo.objects.filter(id=6).update(name="Python从入门到放弃",read_count=88)

#################删除数据#################
# BookInfo.objects.create(
#     name='测试删除数据', author='wipzhu', pub_date='2023-03-24',
#     price=12.8, read_count=10, comment_count=111, is_delete=0
# )
# book=BookInfo.objects.filter(id=7).delete()
