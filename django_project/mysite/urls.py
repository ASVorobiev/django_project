# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [url(r'^admin/service/$', views.my_admin_view),
               url(r'^$', views.events_list, name='events_list'),
               url(r'^adm/$', views.admin_list, name='adm'),
               url(r'^adm/jserv/$', views.jservice, name='jservice'),
               url(r'^jdata/$', views.jdata, name='jdata'),
               url(r'^tag/$', views.set_tags, name='tag_it'),
               url(r'^set_user_location/$', views.set_user_location, name='set_user_location'),
               url(r'^(?P<site_screen_name>[a-z]+)/$', views.events_list, name='location_events'),
               url(r'^add_event_selector/$', views.add_event_selector, name='add_event_selector'),
               url(r'^add_event_form/$', views.add_event_form, name='add_event_form'),
               url(r'^add_successfully/$', views.add_successfully, name='add_successfully'),
               url(r'^add_failed/$', views.add_failed, name='add_failed'),
               url(r'^(?P<site_screen_name>[a-z]+)/(?P<pk>[0-9]+)/(?P<title_translit>[\w\-.%]*)$', views.events_details,
                   name='event_details'),
               ]
