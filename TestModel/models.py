# models.py
# -*-coding:UTF-8-*-
from django.db import models


class Message(models.Model):
    '''留言表'''
    ip = models.CharField(max_length=300, blank=True)
    name = models.CharField(max_length=300)
    email = models.CharField(max_length=300)
    message = models.CharField(max_length=300)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now_add=True)


class Blog(models.Model):
    '''博客表'''
    blog_title = models.CharField(max_length=300)
    blog_content = models.TextField()
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now_add=True)


class spider_article(models.Model):
    '''文章表'''
    title = models.CharField(verbose_name="文章标题", max_length=300)
    linkage = models.CharField(verbose_name="文章链接", max_length=300)
    tag = models.CharField(verbose_name="标签", max_length=300)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now_add=True)

    class Meta:
        ordering = ["create_time"]
        verbose_name = "python文章"
        verbose_name_plural = "python文章"


class Vistor(models.Model):
    '''访问者'''
    ip = models.CharField(verbose_name="访问ip", max_length=300)
    user_agent = models.CharField(verbose_name="user_agent", max_length=300, blank=True)
    country = models.CharField(verbose_name="user_agent", max_length=300, blank=True)
    city = models.CharField(verbose_name="user_agent", max_length=300, blank=True)
    ip_as = models.CharField(verbose_name="user_agent", max_length=300, blank=True)
    isp = models.CharField(verbose_name="user_agent", max_length=300, blank=True)
    count = models.IntegerField(verbose_name="访问次数", default=0)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now_add=True)


# 用户表
class User(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女")
    )

    user_name = models.CharField(max_length=128, unique=True)  # 用户名，唯一
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True, help_text="邮箱")  # 内置邮箱类型，唯一
    sex = models.CharField(max_length=32, choices=gender, default="男")  # 性别只能选男或女，默认男
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)  # 是否邮箱确认

    def __str__(self):  # 人性化显示对象信息
        return self.user_name

    class Meta:
        ordering = ["-create_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:
        ordering = ["-create_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"
