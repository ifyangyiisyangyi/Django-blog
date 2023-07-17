# Create your views here.
import hashlib
import base64


import requests
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from TestModel.models import spider_article
from tool.models import Linkage, Job
from yycode.settings import MOCK_ADDR


def toolview(request):
    return render(request, 'tool/tool.html')


def commdty_code_make_up(request):
    '''
    商品编码补齐
    '''
    return render(request, 'tool/commdty_code_make_up.html')


def sub_table(request):
    '''
    查询分表
    '''
    return render(request, 'tool/sub_table.html')


def mock(request):
    '''
    在线mock工具
    '''
    # print(f'**********   {request.method}   **********')
    # if request.method == 'POST':
    #     return render(request, 'tool/mock.html', context={'mockUrl': 'xxx/xxx'})
    # return render(request, 'tool/mock.html')
    if MOCK_ADDR == 1:
        return render(request, 'tool/mock.html')
    else:
        return HttpResponseRedirect(MOCK_ADDR)


def link_show(request):
    '''
    常用链接
    '''
    linkages = Linkage.objects.all()
    return render(request, 'tool/link_show.html', {'linkages': linkages})


def get_weather(request):
    '''
    获取天气
    '''
    weather_url = f'https://tianqiapi.com/api?version=v6&cityid=101010100&appid=62884591&appsecret=RktG3jTx'
    weather = requests.get(weather_url, timeout=5).json()
    # return render(request, 'tool/get_weather.html', {'weather': weather})
    return render(request, 'tool/get_weather.html', locals())


def article_spider(request):
    articles = spider_article.objects.all()
    article_list = []
    for i in articles:
        article_list.append(i)
    paginator = Paginator(article_list, 12)
    if request.method == "GET":
        page = request.GET.get('page')  # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            articles = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            articles = paginator.page(paginator.num_pages)
    # return render(request, 'tool/article_spider.html', {"articles": articles})
    return render(request, 'tool/article_spider.html', locals())


def md5_func(request):
    if request.method == "POST" :
        str = request.POST.get("md5_str")
        str_md5 = hashlib.md5(str.encode(encoding='utf-8')).hexdigest()
    return render(request, 'tool/md5.html', locals())

def base64_func(request):
    if request.method == "POST" :
        str1 = request.POST.get("base64_str")
        if str1:base64_str = str(base64.b64encode(str1.encode("utf-8")), 'utf-8')
        de_str = request.POST.get("base64_str_de")
        if de_str:base64_str_de = base64.b64decode(de_str).decode("utf-8")
    return render(request, 'tool/base64.html', locals())

def job_func(request):
    jobs = Job.objects.all().order_by("-create_time")[:10]
    if request.method == "POST":
        jobs = Job.objects.filter(tag__contains=request.POST.get("job")).order_by("-create_time")
    job_list = [i for i in jobs]
    paginator = Paginator(job_list, 12)
    if request.method == "GET":
        page = request.GET.get('page')  # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            jobs = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            jobs = paginator.page(paginator.num_pages)
    return render(request, 'tool/job.html', locals())