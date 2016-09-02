# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from mysite import views

urlpatterns = patterns('mysite.views',
                        url(r'^$', views.events_list, name='events_list'),
                        url(r'^add_event_form/$', views.add_event_form, name='add_event_form'),
                        url(r'^event/(?P<pk>[0-9]+)/$', views.events_details, name='event_details')
                       )