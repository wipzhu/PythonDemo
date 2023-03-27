from django.urls import path
from book.views import index, good_list

urlpatterns = [
    # path(路由,视图函数名)
    path('index/', index),
    path('<cat_id>/<goods_id>/', good_list)
]
