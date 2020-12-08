from django.urls import path
from .views import Cbvdemo, Toolview, commdty_code_make_up, sub_table

app_name = 'tool'
urlpatterns = [
    path('', Toolview, name='total'),
    path('Cbvdemo', Cbvdemo.as_view()),
    path('commdty_code_make_up/', commdty_code_make_up, name='commdty_code_make_up'),  # 商品编码自动补齐
    path('sub_table', sub_table, name='sub_table'), # 计算分库分表

]
