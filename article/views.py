# -*- coding: UTF-8 -*-

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .forms import MessageForm, CommentForm, ArticleForm, MessageReplyForm
from .forms import PersonForm, WebintroduceForm
from .models import Article, BlogTags
from .models import Comment, Tags
from .models import Message, Person
from .models import Aboutus, City

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
    about_us = Aboutus.objects.all()[0]
    person = about_us.build_person.split(',')
    http_content = {
        'about_us': about_us,
        'person' : person
    }
    return render(request, 'about.html', http_content)


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
        action = 'edit'
        article = Article.objects.get(id=article_id)
    else:
        article = None
        action = 'create'

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        tags = request.POST.getlist('tags')
        new_tags = set(Tags.objects.filter(id__in=tags))
        if action == 'edit':
            old_tags = set(article.tag.all())
        else:
            old_tags = set([])
        add_tags = new_tags - old_tags
        delete_tags = old_tags - new_tags
        if form.is_valid():
            article_info = form.cleaned_data
            article_info['city_id'] = article_info.pop('city')
            try:
                if action == 'edit':
                    for k, v in article_info.iteritems():
                        setattr(article, k, v)
                else:
                    article = Article.objects.create(**article_info)
                for add_tag in add_tags:
                    BlogTags.objects.create(article_id=article.id, tag=add_tag)
                for delete_tag in delete_tags:
                    BlogTags.objects.filter(article_id=article_id, tag=delete_tag).delete()
                article.save()
                return redirect('/backend_save/?title=3&state=1')
            except:
                return redirect('/backend_save/?title=3&state=0')
    else:
        if action == 'edit':
            form_content = {
                'title': article.title,
                'is_topic': article.is_topic,
                'content': article.content,
            }
            form = ArticleForm(form_content)
        else:
            form = ArticleForm()
    http_content = {
        'title': u'新建博客' if article_id is None else u'博客详情',
        'article': article,
        'form': form,
        'action': action,
    }
    return render(request, 'backend_blog_modify.html', http_content)


def backend_blog_delete(request, blog_id=None):
    blog = Article.objects.get(id=blog_id)
    blog.delete()
    return redirect('/backend_blog_list/')


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
        'title': u'邮件详情',
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
    q = request.GET.get('q', '')
    qry = Q(tag_name__contains=q)
    tags = Tags.objects.filter(qry)
    data = []
    for tag in tags:
        tag_data = {
            'id': tag.id,
            'text': tag.tag_name
        }
        data.append(tag_data)
    return JsonResponse(data, safe=False)


def backend_city_choice(request):
    q = request.GET.get('q', '')
    qry = Q(city_name__contains=q)
    citys = City.objects.filter(qry)
    data = []
    for city in citys:
        city_data = {
            'id': city.id,
            'text': city.city_name
        }
        data.append(city_data)
    return JsonResponse(data, safe=False)


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
                return redirect('/backend_save/?title=1&state=1')
            except:
                return redirect('/backend_save/?title=1&state=0')
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


def backend_save(request):
    title = request.GET.get('title', '')
    state = request.GET.get('state', '')
    title_info = {
        '1': u'个人信息',
        '2': u'网站介绍',
        '3': u'博客详情',
    }
    if state:
        type = u'保存成功 ^_^'
    else:
        type = u'保存失败 T_T'
    http_content = {
        'title': title_info[title],
        'type': type
    }
    return render(request, 'backend_admin_save.html', http_content)


def backend_aboutus(request):
    try:
        about_us = Aboutus.objects.all()[0]
        action = 'edit'
    except:
        action = 'create'

    if request.method == 'POST':
        form = WebintroduceForm(request.POST)
        if form.is_valid():
            introduce_info = form.cleaned_data
            person1 = introduce_info.pop('person1')
            person2 = introduce_info.pop('person2')
            person3 = introduce_info.pop('person3')
            introduce_info['build_person'] = person1 + ',' + person2 + ',' + person3
            try:
                if action == 'create':
                    create_introduce = Aboutus.objects.create(**introduce_info)
                    create_introduce.save()
                else:
                        for k, v in introduce_info.iteritems():
                            setattr(about_us, k, v)
                        about_us.save()
                return redirect('/backend_save/?title=2&state=1')
            except:
                return redirect('/backend_save/?title=2&state=0')
    else:
        if action == 'edit':
            person = about_us.build_person.split(',')
            form_content = {
                'person1': person[0],
                'person2': person[1],
                'person3': person[2],
                'text': about_us.text
            }
            form = WebintroduceForm(form_content)
        else:
            form = WebintroduceForm()
    http_content = {
        'title': u'网站介绍',
        'form': form
    }
    return render(request, 'backend_aboutus.html', http_content)
