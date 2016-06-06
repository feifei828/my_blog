# -*- coding: UTF-8 -*-

from django import forms
from .models import Article


class MessageForm(forms.Form):
    name = forms.CharField(label=u'姓名', initial='', error_messages={'required': u'请输入姓名'})
    email = forms.EmailField(label=u"个人邮箱", initial='',
                             error_messages={'required': u'请输入邮箱', 'invalid': u'请输入正确的邮箱'})
    title = forms.CharField(label=u'主题', initial='', error_messages={'required': u'请输入主题'})
    content = forms.CharField(label=u'内容', initial='', error_messages={'required': u'请输入内容'})


class CommentForm(forms.Form):
    email = forms.EmailField(label=u"个人邮箱", initial='',
                             error_messages={'required': u'请输入邮箱', 'invalid': u'请输入正确的邮箱'})
    comment = forms.CharField(label='评论', initial='', error_messages={'required': u'请输入评论内容'})


class ArticleForm(forms.Form):
    title = forms.CharField(label=u'博客标题', initial='')
    city = forms.CharField(label=u'城市', initial='', required=False)
    is_topic = forms.BooleanField(label=u'是否置于首页', initial='', required=False)
    content = forms.CharField(label=u'博客内容', initial='')

    def clean(self):
        data = self.cleaned_data
        if data['is_topic'] and Article.objects.filter(is_topic=True).count() >= 1:
            self.add_error('is_topic', u'只能有一篇文章在首页')


class MessageReplyForm(forms.Form):
    is_reply = forms.BooleanField(label=u'是否回复', initial='', required=False)


class PersonForm(forms.Form):
    name = forms.CharField(label=u'姓名', initial='')
    email = forms.EmailField(label=u'个人邮箱', initial='')
    phone = forms.CharField(label=u'电话号码', initial='')
    qq = forms.CharField(label=u'qq', initial='', required=False)
    weibo = forms.CharField(label=u'微博地址', initial='', required=False)
    github = forms.CharField(label=u'github', initial='', required=False)


class WebintroduceForm(forms.Form):
    person1 = forms.CharField(label=u'姓名', initial='')
    person2 = forms.CharField(label=u'姓名', initial='', required=False)
    person3 = forms.CharField(label=u'姓名', initial='', required=False)
    text = forms.CharField(label=u'简介', initial='')
