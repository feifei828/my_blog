# -*- coding: UTF-8 -*-

from django.shortcuts import render
from .models import Article
# Create your views here.


def home(request):
    try:
        article = Article.objects.get(is_topic=True)
    except:
        article = Article.objects.order_by('-id').last()

    http_content = {
         'article': article
    }

    return render(request, 'home.html', http_content)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def blog_list(request):
    articles = Article.objects.all()
    http_content = {
        'title': u'博客列表',
        'articles': articles,
    }
    return render(request, 'blog_list.html', http_content)


def blog(request, blog_id=None):
    if blog_id is not None:
        blog = Article.objects.get(id=blog_id)
    http_content = {
        'title': blog.title,
        'blog': blog
    }
    return render(request, 'blog_form.html', http_content)
