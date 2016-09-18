from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^text/$', 'django_project.text_ru.views.base', name='base_send_text'),
                        url(r'^result_send_text/$', 'django_project.text_ru.views.send_text_form', name='result_send_text'),
                        url(r'^jq/$', 'django_project.text_ru.views.advert', name='jq'),
                       )
