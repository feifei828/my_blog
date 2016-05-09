# -*- coding: UTF-8 -*-

from django import forms


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
    content = forms.CharField(label=u'博客内容', initial='')