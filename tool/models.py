from django.db import models


# Create your models here.

class ToolCategory(models.Model):
    name = models.CharField('网站分类名称', max_length=20)
    order_num = models.IntegerField('序号', default=99, help_text='序号可以用来调整顺序，越小越靠前')

    class Meta:
        verbose_name = '工具分类'
        verbose_name_plural = verbose_name
        ordering = ['order_num', 'id']

    def __str__(self):
        return self.name


class ToolLink(models.Model):
    name = models.CharField('网站名称', max_length=20)
    description = models.CharField('网站描述', max_length=100)
    link = models.URLField('网站链接')
    order_num = models.IntegerField('序号', default=99, help_text='序号可以用来调整顺序，越小越靠前')
    category = models.ForeignKey(ToolCategory, verbose_name='网站分类', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = '推荐工具'
        verbose_name_plural = verbose_name
        ordering = ['order_num', 'id']

    def __str__(self):
        return self.name


class Linkage(models.Model):
    name = models.CharField(verbose_name='网站名称', max_length=60)
    link = models.URLField(verbose_name='网站链接')
    clicks = models.IntegerField(verbose_name='点击数', default=0)
    is_top = models.BooleanField(verbose_name='置顶', default=False)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now_add=True)

    class Meta:
        verbose_name = '常用链接'
        verbose_name_plural = verbose_name
        ordering = ['-clicks']

    def __str__(self):
        return self.name[:20]

    def update_clicks(self):
        self.clicks += 1
        self.save(update_fields=['clicks'])

    def get_pre(self):
        return Linkage.objects.filter(id__lt=self.id).order_by('-id').first()

    def get_next(self):
        return Linkage.objects.filter(id__gt=self.id).order_by('id').first()
