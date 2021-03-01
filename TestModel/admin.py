# admin.py

from django.contrib import admin
from TestModel.models import spider_article, User

admin.site.site_header = 'yy 项目管理系统'
admin.site.site_title = '登录系统后台'
admin.site.index_title = '后台管理'


@admin.register(spider_article)
class SpiderAticleAdmin(admin.ModelAdmin):
    list_display = ("title", "linkage", "tag")  # 设置显示的字段
    search_fields = ("title",)  # 搜索条件title
    list_filter = ('tag', 'create_time')  # 激活过滤器


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_name", "email", "sex", "has_confirmed")
    search_fields = ("user_name",)
    list_filter = ("sex", "create_time")
