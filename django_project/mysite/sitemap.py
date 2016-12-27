from django.contrib.sitemaps import Sitemap
from django_project.mysite.models import Events
from django.core.urlresolvers import reverse
from datetime import datetime

class DinamicSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5

    def items(self):
        return Events.objects.filter(is_active=1, export_vk=1, is_deleted=0)

    def lastmod(self, obj):
        return datetime.fromtimestamp(obj.modified)

    # def location(self, obj):
    #     return reverse(obj)


class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ['home']

    def location(self, object):
        return reverse(object)