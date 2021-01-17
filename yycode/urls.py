from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from . import views, spider
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('tool/', include('tool.urls')),
    path('article_spider/', spider.article_spider),
    path('login/', views.login),
    path('captcha/', include('captcha.urls')),  # 图形验证码路由
]

urlpatterns += staticfiles_urlpatterns()
