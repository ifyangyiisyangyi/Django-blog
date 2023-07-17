from django.urls import path

from .views import toolview, commdty_code_make_up, sub_table, mock, link_show, get_weather, article_spider, md5_func, \
    base64_func, job_func

app_name = 'tool'
urlpatterns = [
    path('', toolview, name='total'),
    path('commdty_code_make_up/', commdty_code_make_up, name='commdty_code_make_up'),  # 商品编码自动补齐
    path('sub_table', sub_table, name='sub_table'),  # 计算分库分表
    path('mock', mock, name='mock'),  # 在线mock工具
    path('link_show', link_show, name='link_show'),  # 常用链接
    path('get_weather', get_weather, name='get_weather'),  # 获取天气
    path('article_spider', article_spider, name='article_spider'),  # 爬虫列表
    path('md5', md5_func, name='md5'),  # md5
    path('base64', base64_func, name='base64'),  # base64
    path('job', job_func, name='job'),  # job

]
