from django.contrib import admin

from tool.models import Linkage


# Register your models here.

@admin.register(Linkage)
class LinkageAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_time'
    list_display = ('id', 'name', 'link', 'clicks', 'create_time', 'update_time', 'is_top')
    exclude = ('clicks',)
    list_display_links = ('name',)
    list_filter = ('create_time', 'is_top')
