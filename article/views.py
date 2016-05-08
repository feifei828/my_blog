# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.shortcuts import redirect
from .models import Article
from .models import Message
from .models import Comment
from .forms import MessageForm
from .forms import CommentForm
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
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            contact_info = form.cleaned_data
            try:
                message = Message.objects.create(**contact_info)
                message.save()
                return redirect('/contact_success')
            except:
                return redirect('/contact_error')

    else:
        form = MessageForm()

    http_content = {
        'title': u'与我联系',
        'form': form
    }
    return render(request, 'contact.html', http_content)


def contact_success(request):
    http_content = {
        'title': u'发送成功'
    }
    return render(request, 'contact_success.html', http_content)


def contact_error(request):
    http_content = {
        'title': u'发送失败'
    }
    return render(request, 'contact_error.html', http_content)


def blog_list(request, srch_val=None):
    try:
        articles = Article.objects.filter(title__contains=srch_val)
    except:
        articles = Article.objects.all()
    http_content = {
        'title': u'博客列表',
        'articles': articles,
    }
    return render(request, 'blog_list.html', http_content)


def blog_modify(request, blog_id=None):
    if blog_id is not None:
        blog = Article.objects.get(id=blog_id)
        comments = Comment.objects.filter(article=blog)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            contact_info = form.cleaned_data
            contact_info['article'] = blog
            try:
                message = Comment.objects.create(**contact_info)
                message.save()
                return redirect('/contact_success')
            except:
                return redirect('/contact_error')
    else:
        form = CommentForm()

    http_content = {
        'title': blog.title,
        'blog': blog,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog_modify.html', http_content)


def backend(request):
    return render(request, 'backend_home.html')