from django.urls import path
from book.views import good_list, register, json

urlpatterns = [
    # path(路由,视图函数名)
    path('register/', register),
    path('goods/<cat_id>/<goods_id>/', good_list),
    path('json/', json),
]
