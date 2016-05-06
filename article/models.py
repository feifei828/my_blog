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
