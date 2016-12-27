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


from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps.views import sitemap

from django_project import settings
from django_project.mysite import admin
from django_project.mysite.sitemap import DinamicSitemap, StaticSitemap

sitemaps = {'events': DinamicSitemap}

urlpatterns = [url(r'', include('django_project.user_auth.urls')),
               url(r'', include('django_project.text_ru.urls')),
               url(r'', include('social.apps.django_app.urls', namespace='social')),
               # url(r'^admin/', include(admin.)),
               url(r'', include('django_project.about.urls')),
               url(r'', include('django_project.mysite.urls')),
                url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
                    name='django.contrib.sitemaps.views.sitemap')
               ]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
