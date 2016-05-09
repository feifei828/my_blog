# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from .models import Article
from .models import Message
from .models import Comment
from .forms import MessageForm, CommentForm, ArticleForm
# Create your views here.


def blog_login(request):
    err_msg = ''
    if request.user.is_authenticated():
        return redirect('/backend_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        session = authenticate(username=username, password=password)
        if session is not None:
            login(request, session)
            return redirect('/backend_home')

        err_msg = u'用户名或密码错误'

    http_content = {
        'err_msg': err_msg,
    }

    return render(request, 'login.html', http_content)


def blog_logout(request):
    logout(request)
    return redirect('/home')


def home(request):
    try:
        article = Article.objects.get(is_topic=True)
    except:
        article = Article.objects.order_by('-id').last()

    http_content = {
         'article': article
    }
    print(request.user)
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


def backend_home(request):
    http_content = {
        'title': u'首页'
    }
    return render(request, 'backend_home.html', http_content)


def backend_blog_list(request):
    articles = Article.objects.all()
    http_content = {
        'title': u'博客列表',
        'articles': articles,
    }
    return render(request, 'backend_blog_list.html', http_content)


def backend_blog_modify(request, article_id=None):
    if article_id is not None:
        article = Article.objects.get(id=article_id)

        form_content = {
            'content': article.content
        }
    form = ArticleForm(form_content)
    print(form)
    http_content = {
        'title': u'博客详情',
        'article': article,
        'form': form,
    }
    return render(request, 'backend_blog_modify.html', http_content)
