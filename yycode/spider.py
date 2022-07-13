import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse

from TestModel.models import spider_article
from blog.views import log


def get_article_page(url):
    r = requests.request('get', url=url)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    ls = soup('h3', class_="com-article-panel-title")
    url_dict = {}
    for tag in ls:
        s = 'https://cloud.tencent.com' + tag.a['href']
        title = tag.a.string
        obj = spider_article.objects.filter(title=title).first()  # 查询文章是否已存在
        if obj == None:
            article = spider_article(title=title,
                                     linkage=s,
                                     tag="python")
            article.save()
            log.info(f'保存文章 --> {title}')
        else:
            log.info(f'已存在文章 --> {title}')
        url_dict[title] = s  # 返回文章的标题和链接
    return url_dict


def article_spider(request):
    url_dict = {}
    for i in range(30):
        url = 'https://cloud.tencent.com/developer/column/5263/page-' + str(i + 1)
        log.info(f'-------------------->> 抓取第{i + 1}页')
        url_sigle_dict = get_article_page(url)
        url_dict = dict(url_dict, **url_sigle_dict)
    return JsonResponse(url_dict)


# 码霸霸

def get_mababa_article_page(url):
    r = requests.get(url=url)
    html = r.text
    print(html)
    soup = BeautifulSoup(html, 'lxml')
    ls = soup('article', class_="post")
    url_dict = {}
    for tag in ls:
        title = tag.header.h2.a.string.strip()
        s = tag.header.h2.a["href"]
        obj = spider_article.objects.filter(title=title).first()  # 查询文章是否已存在
        if obj == None:
            article = spider_article(title=title,
                                     linkage=s,
                                     tag="java")
            try:
                article.save()
                log.info(f'保存文章 --> {title}')
            except:
                log.info(f'存表异常 --> {title}')
        else:
            log.info(f'已存在文章 --> {title}')
        url_dict[title] = s
    return url_dict


def mababa_spider(request):
    url_dict = {}
    for i in range(5):
        url = 'https://blog.lupf.cn/?p=' + str(i + 1)
        log.info(f'-------------------->> 抓取第{i + 1}页')
        url_sigle_dict = get_mababa_article_page(url)
        url_dict = dict(url_dict, **url_sigle_dict)
    return JsonResponse(url_dict)
