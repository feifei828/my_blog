# -*- coding: UTF-8 -*-
from django import forms


class BlogForm(forms.Form):
    title = forms.CharField(label=u'标题', max_length=128, initial='')