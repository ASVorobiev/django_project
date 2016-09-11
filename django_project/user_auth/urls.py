from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
                       #url(r'^$', 'example.app.views.home'),
    url(r'^admin/', include(admin.site.urls)),
                       url(r'^email-sent/', 'django_project.user_auth.views.validation_sent'),
                       url(r'^login/$', 'django_project.user_auth.views.home', name='login'),
                       url(r'^logout/$', 'django_project.user_auth.views.logout', name='logout'),
                       url(r'^done/$', 'django_project.user_auth.views.done', name='done'),
                       url(r'^ajax-user_auth/(?P<backend>[^/]+)/$', 'django_project.user_auth.views.ajax_auth',
                           name='ajax-user_auth'),
                       url(r'^email/$', 'django_project.user_auth.views.require_email', name='require_email'),
                       url(r'', include('social.apps.django_app.urls', namespace='social'))
                       )
