import logging
import time
import markdown
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.views import generic
from markdown.extensions.toc import TocExtension, slugify
from TestModel.models import Vistor
from blog.models import Article, Category, Tag
from yycode.settings import NEVER_REDIS_TIMEOUT

log = logging.getLogger(name='blog')


class IndexView(generic.ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', 10)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self):
        log.info(f'******请求header****** : {self.request.META}')
        save_vistor(self.request)  # 保存访问者ip
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ('-is_top', '-create_date')


class DetailView(generic.DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'

    def get_object(self):
        obj = super(DetailView, self).get_object()
        # 设置浏览量增加时间判断,同一篇文章两次浏览超过5分钟才重新统计阅览量,作者浏览忽略
        u = self.request.user
        ses = self.request.session
        the_key = 'is_read_{}'.format(obj.id)
        is_read_time = ses.get(the_key)
        if u != obj.author:
            if not is_read_time:
                obj.update_views()
                ses[the_key] = time.time()
            else:
                now_time = time.time()
                t = now_time - is_read_time
                if t > 60 * 5:
                    obj.update_views()
                    ses[the_key] = time.time()
        # 获取文章更新的时间，判断是否从缓存中取文章的markdown,可以避免每次都转换
        ud = obj.update_date.strftime("%Y%m%d%H%M%S")
        md_key = '{}_md_{}'.format(obj.slug, ud)
        cache_md = cache.get(md_key)
        if cache_md:
            log.info(f'从缓存中取出 : {cache_md}')
            obj.body, obj.toc = cache_md
        else:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                TocExtension(slugify=slugify),
            ])
            obj.body = md.convert(obj.body)
            obj.toc = md.toc
            # cache.set(md_key, (obj.body, obj.toc), 60 * 60 * 12)
            cache.set(md_key, (obj.body, obj.toc), NEVER_REDIS_TIMEOUT)  # 缓存一年文章
        # print(f"打印:{obj}")
        return obj


class CategoryView(generic.ListView):
    model = Article
    template_name = 'blog/category.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self):
        ordering = super(CategoryView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ordering

    def get_queryset(self, **kwargs):
        queryset = super(CategoryView, self).get_queryset()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return queryset.filter(category=cate)

    def get_context_data(self, **kwargs):
        context_data = super(CategoryView, self).get_context_data()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context_data['search_tag'] = '文章分类'
        context_data['search_instance'] = cate
        return context_data


class TagView(generic.ListView):
    model = Article
    template_name = 'blog/tag.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self):
        ordering = super(TagView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ordering

    def get_queryset(self, **kwargs):
        queryset = super(TagView, self).get_queryset()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return queryset.filter(tags=tag)

    def get_context_data(self, **kwargs):
        context_data = super(TagView, self).get_context_data()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        context_data['search_tag'] = '文章标签'
        context_data['search_instance'] = tag
        return context_data


def save_vistor(request):
    '''
    保存访问者ip
    '''
    try:
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
        else:
            ip = request.META['REMOTE_ADDR'].split(',')[0]
        if ip == '127.0.0.1':
            log.info(f'本地请求 --> {ip}')
        else:
            if "HTTP_USER_AGENT" in request.META:
                user_agent = request.META['HTTP_USER_AGENT']
            else:
                user_agent = ""
            vistor = Vistor(ip=ip, user_agent=user_agent, count=3)
            log.info(f'ip && user_agent : {vistor.ip} && {vistor.user_agent}')
            if ',' in vistor.ip:
                log.error(f'异常IP : {vistor.ip}')
                mail_reminder("异常IP", f'异常ip --> {vistor.ip}')
            vistor.save()
    except:
        log.error("保存ip失败!")


# 通用邮件提醒
def mail_reminder(sub, mes):
    send_mail(sub, mes, '117645743@qq.com', ['937471204@qq.com'])
