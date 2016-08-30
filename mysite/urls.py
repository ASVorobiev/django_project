# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from mysite import views

urlpatterns = patterns('mysite.views',
    #url(r'^list/$', 'list', name='list'),
    url(r'^$', views.post_list, name='post_list'),
)