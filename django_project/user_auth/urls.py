from django.conf.urls import include, url
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = (url(r'^admin/', include(admin.site.urls)),
               url(r'^email-sent/', views.validation_sent),
               url(r'^login/$', views.home, name='login'),
               url(r'^logout/$', views.logout, name='logout'),
               url(r'^done/$', views.done, name='done'),
               url(r'^ajax-user_auth/(?P<backend>[^/]+)/$', views.ajax_auth, name='ajax-user_auth'),
               url(r'^email/$', views.require_email, name='require_email'),
               url(r'', include('social.apps.django_app.urls', namespace='social')),
               )
