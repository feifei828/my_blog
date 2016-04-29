# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function
from django.db import models

# Create your models here.


class Article(models.Model):
    class Meta:
        verbose_name = u'博客文章'

    title = models.CharField(verbose_name=u'博客标题', max_length=128, null=False)
    tag = models.CharField(verbose_name=u'博客标签', max_length=50, blank=True)
    date_time = models.DateTimeField(verbose_name=u'博客日期', auto_now_add=True)
    content = models.TextField(verbose_name=u'博客正文', blank=True, null=True)
    local = models.CharField(verbose_name=u'位置', max_length=20, blank=True)
    is_topic = models.BooleanField(verbose_name=u'是否显示在首页', default=False)

    def __unicode__(self):
        return self.title
