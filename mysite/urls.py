# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from mysite import views

urlpatterns = patterns('mysite.views',
                       #url(r'^list/$', 'list', name='list'),
    url(r'^$', views.events_list, name='post_list'),
    url(r'^add_event_form/$', views.add_event_form, name='add_event_form'),
                       )