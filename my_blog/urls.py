# -*- coding: UTF-8 -*-
"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from article.views import home, about, contact, blog_list, blog_modify, backend_home, \
                            contact_success, contact_error, blog_login, blog_logout, \
                            backend_blog_list, backend_blog_modify
import settings

urlpatterns = [
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^login/$', blog_login),
    url(r'^logout/$', blog_logout),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', home),
    url(r'^about/$', about),
    url(r'^contact/$', contact),
    url(r'^contact_success/$', contact_success),
    url(r'^contact_error/$', contact_error),
    url(r'^blog_list/$', blog_list),
    url(r'^blog_list/(.+)/$', blog_list),
    url(r'^modify/(.+)/$', blog_modify,),
    url(r'^backend_home/$', backend_home),
    url(r'^backend_blog_list/$', backend_blog_list),
    url(r'^backend_blog_modify/(.+)$', backend_blog_modify),

]
