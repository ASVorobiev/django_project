# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
                       url(r'^$', views.events_list, name='events_list'),
                       url(r'^adm/$', views.admin_list, name='adm'),
                       url(r'^jdata/$', views.jdata, name='jdata'),
                       url(r'^(?P<site_screen_name>[a-z]+)/$', views.events_list, name='location_events'),
                       url(r'^add_event_form/$', views.add_event_form, name='add_event_form'),
                       url(r'^(?P<site_screen_name>[a-z]+)/event(?P<pk>[0-9]+)/(?P<title_translit>[\w\-.%]+)$', views.events_details, name='event_details'),
                       ]
