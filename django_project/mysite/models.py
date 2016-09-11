from django.conf.urls import patterns
from django.db import models

# Create your models here.
from django.forms import ModelForm
from django.shortcuts import redirect
from django.utils.datetime_safe import datetime
from django.utils.safestring import mark_safe


class Locations(models.Model):
    name = models.CharField(max_length=255)
    vk_group_id = models.IntegerField(blank=True, null=True)
    vk_screen_name = models.CharField(max_length=255, blank=True, null=True)
    vk_owner_id = models.IntegerField(blank=True, null=True)
    vk_location_event_id = models.IntegerField(blank=True, null=True)
    tz = models.IntegerField(blank=True, null=True)
    is_deleted = models.IntegerField()
    modified = models.IntegerField()
    created = models.IntegerField()

    def __str__(self):
        return self.name


class Events(models.Model):
    location = models.ForeignKey(Locations)
    title = models.CharField(max_length=255, verbose_name='заголовок')
    description = models.TextField(blank=True, verbose_name='описание')
    image = models.ImageField(max_length=255, blank=True, null=True, verbose_name='афиша')
    thumb = models.CharField(max_length=255, blank=True, null=True, verbose_name='предпросмотр афиши')
    category_id = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(verbose_name='дата начала')
    start_time = models.TimeField(verbose_name='время начала')
    duration = models.IntegerField(blank=True, null=True)
    finish_date = models.DateField(blank=True, null=True)
    is_perodic = models.IntegerField(blank=True, null=True, choices=((0, 'No'), (1, 'Yes')))
    shedule = models.CharField(max_length=255, blank=True, null=True)
    place_id = models.IntegerField(blank=True, null=True)
    place_comment = models.CharField(max_length=255, blank=True, null=True)
    organizer_id = models.IntegerField(blank=True, null=True)
    is_free = models.IntegerField(blank=True, null=True)
    tickets = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    priority = models.IntegerField(choices=((0, 'Normal'),
                                            (1, 'Proirity')), default=0)
    is_active = models.IntegerField(choices=((0, 'No'), (1, 'Yes')), default=1)
    export_vk = models.IntegerField(choices=((0, 'No'), (1, 'Yes')), default=1)
    is_deleted = models.IntegerField(choices=((0, 'No'), (1, 'Yes')), default=0)
    created = models.IntegerField(default=int(datetime.utcnow().timestamp()))
    modified = models.IntegerField(default=int(datetime.utcnow().timestamp()))

    def image_small(self):
        if self.image:
            return mark_safe('<img src="%s" width="150" height="150" />' % self.image.url)
        else:
            return '(none)'
    image_small.short_description = 'Thumb'
    image_small.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        my_urls = patterns('',
                           (r'^(?P<pk>\d+)/events/$', self.admin_site.admin_view(self.do_evil_view))
                           )
        return my_urls + urls

    def do_evil_view(self, request, pk):
        print('doing evil with', Events.objects.get(pk=int(pk)))
        return redirect('/admin/mysite/events/%s/' % pk)

    def __str__(self):
        return self.title


class LocationCities(models.Model):
    vk_city_id = models.IntegerField(primary_key=True)
    location_id = models.IntegerField()
    vk_city_name = models.CharField(max_length=255)


class MysiteCategories(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'mysite_categories'


class MysiteOrganizers(models.Model):
    vk_id = models.IntegerField(blank=True, null=True)
    vk_type = models.CharField(max_length=5, blank=True, null=True)
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    followers = models.IntegerField(blank=True, null=True)
    place_id = models.IntegerField(blank=True, null=True)
    confidence = models.IntegerField()
    is_deleted = models.IntegerField()
    modified = models.IntegerField()
    created = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mysite_organizers'
        unique_together = (('vk_id', 'vk_type'),)


class MysitePlaces(models.Model):
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)
    lat = models.FloatField(blank=True, null=True)
    lan = models.FloatField(blank=True, null=True)
    is_deleted = models.IntegerField()
    modified = models.IntegerField()
    created = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mysite_places'
