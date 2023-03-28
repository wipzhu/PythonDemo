from django.urls import path, converters
from django.urls.converters import register_converter
from book.views import good_list, register, json, shop, response, setCookie, getCookie


class MobileConverter:
    regex = '1[3-9]\d{9}'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


# 注册转换器
register_converter(MobileConverter, 'phone')

urlpatterns = [
    # path(路由,视图函数名)
    # <转换器名名字:变量名>
    path('shop/<int:city_id>/<phone:mobile>', shop),
    path('goods/<int:cat_id>/<int:goods_id>/', good_list),
    path('register/', register),
    path('json/', json),
    path('response/', response),
    path('set-cookie/', setCookie),
    path('get-cookie/', getCookie),
]
