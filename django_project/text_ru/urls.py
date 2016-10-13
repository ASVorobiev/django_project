from django.conf.urls import include, url
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = [url(r'^text/$', views.base, name='base_send_text'),
               url(r'^result_send_text/$', views.send_text_form, name='result_send_text'),
               url(r'^jq/$', views.advert, name='jq'),
               ]
