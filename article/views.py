# -*- coding: UTF-8 -*-

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import MessageForm, CommentForm, ArticleForm, MessageReplyForm
from .forms import PersonForm
from .models import Article
from .models import BlogTags
from .models import Comment, Tags
from .models import Message
from .models import Person


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
    return render(request, 'home.html', http_content)


def about(request):

    return render(request, 'about.html')


def contact(request):
    person = Person.objects.all()[0]
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
        'form': form,
        'person': person,
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

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article_info = form.cleaned_data
            for k, v in article_info.iteritems():
                setattr(article, k, v)
            article.save()
    else:
        form_content = {
            'title': article.title,
            'is_topic': article.is_topic,
            'content': article.content,
        }
        form = ArticleForm(form_content)
    http_content = {
        'title': u'博客详情',
        'article': article,
        'form': form,
    }
    return render(request, 'backend_blog_modify.html', http_content)


def backend_blog_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article_info = form.cleaned_data
            try:
                article = Article.objects.create(**article_info)
                article.save()
                return redirect('/backend_blog_list')
            except:
                return redirect('/backend_blog_create')

    http_content = {
        'title': u'新建博客',
    }
    return render(request, 'backend_blog_modify.html', http_content)


def backend_messages(request):
    messages = Message.objects.all()
    http_content = {
        'title': u'收到邮件',
        'messages': messages,
    }
    return render(request, 'backend_messages.html', http_content)


def backend_messages_modify(request, message_id=None):
    if message_id is not None:
        message = Message.objects.get(id=message_id)

    if request.method == 'POST':
        form = MessageReplyForm(request.POST)
        if form.is_valid():
            message_info = form.cleaned_data
            for k, v in message_info.iteritems():
                setattr(message, k, v)
            message.save()
    else:
        form_content = {
            'is_reply': message.is_reply
        }
        form = MessageReplyForm(form_content)

    http_content = {
        'title': u'消息详情',
        'message': message,
        'form': form
    }
    return render(request, 'backend_message_modify.html', http_content)


def backend_tags(request):
    tags = Tags.objects.all()
    tags_info = []

    for tag in tags:
        tag_content = {}
        count = BlogTags.objects.filter(tag_id=tag.id).count()
        tag_content['id'] = tag.id
        tag_content['name'] = tag.tag_name
        tag_content['count'] = count
        tags_info.append(tag_content)

    http_content = {
        'title': u'标签管理',
        'tags': tags_info,
    }
    return render(request, 'backend_tags.html', http_content)


def backend_tags_create(request):
    if request.method == 'POST':
        tag_name = request.POST.get('tag_name')
        try:
            tag = Tags.objects.create(tag_name=tag_name)
            tag.save()
            return redirect('/backend_tags')
        except:
            return redirect('/backend_tags_create')

    http_content = {
        'title': u'新建标签'
    }
    return render(request, 'backend_tags_create.html', http_content)


def backend_tag_delete(request, tag_id=None):
    tag = Tags.objects.get(id=tag_id)
    tag.delete()
    return redirect('/backend_tags')


def backend_tag_choice(request):
    tags =Tags.objects.all()
    data = []
    for tag in tags:
        tag_data = {
            'id': tag.id,
            'text': tag.tag_name
        }
        data.append(tag_data)
    return data


def backend_admin(request):
    try:
        person = Person.objects.all()[0]
    except:
        person = Person
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person_info = form.cleaned_data
            try:
                for k, v in person_info.iteritems():
                    setattr(person, k, v)
                person.save()
                return redirect('/backend_admin_save/1')
            except:
                return redirect('/backend_admin_save/0')
    else:
        form_info = {
            'name': person.name,
            'email': person.email,
            'phone': person.phone,
            'qq': person.qq,
            'weibo': person.weibo,
            'github': person.github,
        }
        form = PersonForm(form_info)

    http_content = {
        'title': u'个人信息',
        'form': form,
    }
    return render(request, 'backend_admin.html', http_content)


def backend_admin_save(request, type_id=None):
    if type_id:
        type = u'保存成功 ^_^'
    else:
        type = u'保存失败 T_T'
    http_content = {
        'title': u'个人信息',
        'type': type
    }
    return render(request, 'backend_admin_save.html', http_content)
