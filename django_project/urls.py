"""django_project URL Configuration

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
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from mysite import views

urlpatterns = patterns('',
    url(r'', include('mysite.urls')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^$', 'example.app.views.home'),
    url(r'^email-sent/', 'example.app.views.validation_sent'),
    url(r'^login/$', 'example.app.views.home'),
    url(r'^logout/$', 'example.app.views.logout'),
    url(r'^done/$', 'example.app.views.done', name='done'),
    url(r'^ajax-auth/(?P<backend>[^/]+)/$', 'example.app.views.ajax_auth', name='ajax-auth'),
    url(r'^email/$', 'example.app.views.require_email', name='require_email'),

)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)