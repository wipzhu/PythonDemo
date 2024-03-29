from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse

# Create your views here.
"""视图函数有两个要求：
1、第一个参数是接收请求
2、必须返回响应
"""


########################urls###########################
def index(request):
    context = {
        'title': '戳我去百度',
        'name': '马上双十一了，戳我有惊喜~'
    }
    return render(request, 'book/index.html', context)
    # return HttpResponse('Success')


########################test_urls###########################
def shop(request, city_id, mobile):
    print(city_id)
    print(mobile)
    return HttpResponse('Success')


def good_list(request, cat_id, goods_id):
    print(cat_id + goods_id)
    params = request.GET
    print(params)
    order = params.get('order')
    print(order)
    order = params.getlist('order')
    print(order)

    return HttpResponse(cat_id + goods_id)


def register(request):
    params = request.POST
    print(params)
    return JsonResponse(params)


def json(request):
    data = request.body
    data_str = data.decode()
    print(data_str)
    # json形式的字符串可以转换为字典
    import json
    body_dict = json.loads(data_str)
    print(body_dict)
    # return JsonResponse(data_str, safe=False)

    headers = request.META
    print(headers['SERVER_NAME'])
    print(headers['SERVER_PORT'])
    print(request.method)
    return HttpResponse('json')


def response(request):
    # response = HttpResponse('Success', status=200)
    # response['name'] = 'wipzhu'
    # return response
    from django.http import JsonResponse
    info = {
        'name': 'wipzhu',
        'age': 28
    }
    response = JsonResponse(data=info)
    friends = [
        {
            'name': 'Jack',
            'address': 'shanghai'
        },
        {
            'name': 'Rose',
            'address': 'beijing'
        }
    ]
    # response = JsonResponse(data=friends, safe=False)
    # return response

    return redirect('https://www.baidu.com/')


def setCookie(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    res = HttpResponse('Success')
    res.set_cookie('username', username, max_age=3600)
    res.set_cookie('password', password)
    # 删除cookie
    # res.delete_cookie(username)
    return res


def getCookie(request):
    cookie = request.COOKIES
    name = cookie.get('username')
    print(name)
    return HttpResponse(name)


def setSession(request):
    username = request.GET.get('username')
    user_id = 123456
    request.session['username'] = username
    request.session['userid'] = user_id

    # 清除session
    # request.session.delete()
    # request.session.clear()  # 清除key，保留value
    # request.session.flush()  # key和value全清除

    request.session.set_expiry(250)

    return HttpResponse("Success")


def getSession(request):
    userid = request.session.get('userid')
    username = request.session.get('username')

    content = '{},{}'.format(userid, username)
    return HttpResponse(content)


def testLogin(request):
    print(request.method)
    if request.method == 'GET':
        return HttpResponse("GET")
    elif request.method == 'POST':
        return HttpResponse("POST")


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


from django.contrib.auth.mixins import LoginRequiredMixin


# 多继承，注意继承的先后顺序
class OrderView(LoginRequiredMixin, View):

    def get(self, request):
        # isLogin = False
        # if not isLogin:
        #     return HttpResponse("这个页面需要登录才能访问，请先登录")

        return HttpResponse('Order Get，页面必须登录')

    def post(self, request):
        return HttpResponse('Order Post，页面必须登录')

# from book.models import BookInfo, PeopleInfo
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

#################查找数据#################
# try:
#     book = BookInfo.objects.get(id=7)
# except BookInfo.DoesNotExist:
#     print("查询结果不存在")
# from book.models import PeopleInfo
# all = PeopleInfo.objects.all()
# count = all.count()
# 过滤查询：模型类名.objects.filter(属性名__运算符=值),
# 模型类名.objects.exclude(属性名__运算符=值)
# 模型类名.objects.get(属性名__运算符=值)
# BookInfo.objects.get(pk=1)
# BookInfo.objects.filter(pk=1)
# BookInfo.objects.filter(name__contains='湖')  # 书名中包含xx
# BookInfo.objects.filter(name__endswith='部')  # 书名以xx结尾
# BookInfo.objects.filter(name__isnull=True)  # 书名为Null
# BookInfo.objects.filter(id__in=[1, 2, 3])  # id在列表内
# BookInfo.objects.filter(id__gte=3)  # id >=
# BookInfo.objects.exclude(id=3)  # id != 3
# BookInfo.objects.filter(pub_date__year=1980)  # 1980年 发表的图书
# BookInfo.objects.filter(pub_date__gt='1990-01-01')  # 1990-01-01后发表的图书
#
# from django.db.models import F, Q
#
# BookInfo.objects.filter(read_count__gte=(F('comment_count') * 2))  # 阅读数 >= 2 * 评论数
# BookInfo.objects.filter(read_count__gte=20, id__lt=4)  # 多条件
# BookInfo.objects.filter(Q(read_count__gte=80) & Q(id__gt=2))  # 逻辑条件
# BookInfo.objects.filter(~Q(id=3))  # id != 3
#
# #################聚合函数#################
# from django.db.models import Sum, Avg, Max, Min, Count
#
# BookInfo.objects.aggregate(Count('id'))
# BookInfo.objects.aggregate(Avg('read_count'))
#
# #################排序#################
# BookInfo.objects.all().order_by('-read_count')  # 倒序，字段名字前加"-"
#
# #################关联查询#################
# book = BookInfo.objects.get(id=1)
# people = book.peopleinfo_set.all()
# people1 = PeopleInfo.objects.filter(book=1)
#
# # 查询任务为1的书籍信息
# person = PeopleInfo.objects.get(id=1)
# bookInfo = person.book
# bookName = bookInfo.name
#
# #################关联过滤查询#################
# # 查询图书，要求图书人物为”郭靖”
# BookInfo.objects.filter(peopleinfo__name="郭靖")
# # 查询图书，要求图书中人物描述包含”八“
# BookInfo.objects.filter(peopleinfo__description__contains="八")
#
# # 查询书名为“天龙八部”的所有人物
# PeopleInfo.objects.filter(book__name="天龙八部")
# # 查询图书阅读量>30的所有人物
# PeopleInfo.objects.filter(book__read_count__gt=30)
# PeopleInfo.objects.filter(book__read_count__gt=30)[2:5]  # 分页查询
#
# from django.core.paginator import Paginator
#
# peoples = PeopleInfo.objects.all().order_by('id')
# p = Paginator(peoples, 2)  # 每页条数
# page_people = p.page(1)  # 页码
