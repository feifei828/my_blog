# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

# Create your models here.


class Tags(models.Model):
    class Meta:
        verbose_name = u'标签'

    tag_name = models.CharField(verbose_name='标签类型', max_length=20)

    def __unicode__(self):
        return self.tag_name


class Province(models.Model):
    class Meta:
        verbose_name = u'省/直辖市'
    province_name = models.CharField(verbose_name=u'省/直辖市名称', max_length=20)

    def __unicode__(self):
        return self.tag_name


class City(models.Model):
    class Meta:
        verbose_name = u'城市'

    province = models.ForeignKey(Province, verbose_name=u'所在省')
    city_name = models.CharField(verbose_name=u'城市名称', max_length=20, default='')

    def __unicode__(self):
        return self.city_name


class Article(models.Model):
    class Meta:
        verbose_name = u'博客文章'

    title = models.CharField(verbose_name=u'博客标题', max_length=128, null=False)
    tag = models.ManyToManyField(Tags, verbose_name=u'博客标签', related_name='articles', through='BlogTags')
    update_time = models.DateTimeField(verbose_name=u'博客日期', auto_now=True)
    content = models.TextField(verbose_name=u'博客正文', blank=True, null=True)
    city = models.ForeignKey(City, verbose_name=u'所在城市')
    is_topic = models.BooleanField(verbose_name=u'是否显示在首页', default=False)

    def __unicode__(self):
        return self.title


class BlogTags(models.Model):
    class Meta:
        verbose_name = u'标签'

    article = models.ForeignKey(Article)
    tag = models.ForeignKey(Tags)


class Comment(models.Model):
    class Meata:
        verbose_name = u'博客评论'
    article = models.ForeignKey(Article, verbose_name=u'关联博客',related_name='comment')
    email = models.EmailField(verbose_name=u'评论所用邮箱', max_length=100)
    comment = models.TextField(verbose_name=u'评论内容', blank=True, null=True)


class Message(models.Model):
    class Meta:
        verbose_name = u'消息'

    name = models.CharField(verbose_name=u'姓名', max_length=128)
    email = models.EmailField(verbose_name=u"个人邮箱", max_length=100)
    create_time = models.DateTimeField(verbose_name=u'发送时间', auto_now_add=True)
    title = models.CharField(verbose_name=u'主题', max_length=128)
    content = models.TextField(verbose_name=u'信息内容', blank=True)
    is_reply = models.BooleanField(verbose_name=u'是否回复', default=False)